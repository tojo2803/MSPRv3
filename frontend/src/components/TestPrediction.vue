<template>
  <div>
    <div>
    <h1>{{ $t('testprediction_title') }}</h1>
    <label for="region">{{ $t('testprediction_choose_region') }}</label>
    <select v-model="selectedRegion" id="region">
      <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
    </select>
  </div>
  <div>
    <label for="pays">{{ $t('testprediction_choose_country') }}</label>
    <select v-model="selectedPays" id="pays">
      <option v-for="pays in paysList" :key="pays.id" :value="pays.nom">{{ pays.nom }}</option>
    </select>
  </div>
  <div>
    <label for="table">{{ $t('testprediction_choose_table') }}</label>
    <select v-model="selectedTable" id="table" @change="fetchColumns">
      <option v-for="table in tables" :key="table" :value="table">{{ table }}</option>
    </select>
  </div>
  <div>
    <label for="target_column">{{ $t('testprediction_choose_column') }}</label>
    <select v-model="selectedColumn" id="target_column" v-if="columns.length > 0">
      <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
    </select>
  </div>

    <button @click="submitChoices" :disabled="!selectedTable || !selectedColumn">
      {{ $t('testprediction_submit') }}
    </button>
  </div>
</template>

<script>
import apiClient from "/services/api";
import { usePredictionStore } from '@/stores/predictionStore';

export default {
data() {
  return {
    regions: [],
    paysList: [],
    tables: [],
    columns: [],
    selectedRegion: null,
    selectedPays: null,
    selectedTable: null,
    selectedColumn: null,
    predictionResult: null,
  };
},
async mounted() {
  try {
    const responseTables = await apiClient.get("/tables/");
    console.log(this.$t('testprediction_log_tables'), responseTables.data);
    this.tables = Object.keys(responseTables.data.tables);

    const responsePays = await apiClient.get("/payslist/");
    console.log(this.$t('testprediction_log_countries'), responsePays.data);
    const pays = responsePays.data;
    this.paysList = pays;

    const regionsSet = new Set(pays.map(p => p.region));
    this.regions = [...regionsSet]; // dédoublonné

  } catch (error) {
    console.error(this.$t('testprediction_error_load'), error);
  }
},
methods: {
  async fetchColumns() {
    if (!this.selectedTable) return;

    try {
      const response = await apiClient.get(`/columns/${this.selectedTable}`);
      this.columns = response.data.columns;
      console.log(this.$t('testprediction_log_columns'), this.columns);
    } catch (error) {
      console.error(this.$t('testprediction_error_columns'), error);
    }
  },
  async submitChoices() {
    const payload = {
      region: this.selectedRegion || null,
      pays: this.selectedPays || null,
      table: this.selectedTable,
      target_column: this.selectedColumn,
    };

    console.log(this.$t('testprediction_log_payload'), payload); 
    if (!payload.region && !payload.pays) {
      console.error(this.$t('testprediction_error_select'));
      alert(this.$t('testprediction_alert'));
      return;
    }

    try {
    const response = await apiClient.post("/dataframe/", payload);
    const dataframe = response.data.dataframe;
    console.log(this.$t('testprediction_log_dataframe'), response.data);

    const trainPayload = {
      dataframe,
      target_column: payload.target_column,
    };
    console.log(this.$t('testprediction_log_train_payload'), trainPayload);

    const trainResponse = await apiClient.post("/train_model/", trainPayload);
    console.log(this.$t('testprediction_log_success'), trainResponse.data);

    // Stocke le résultat dans le store
    const predictionStore = usePredictionStore();
    predictionStore.setResult(trainResponse.data);

    // Stocke le résultat dans une variable pour l'afficher ou le transmettre
    this.predictionResult = trainResponse.data; // Ajoute predictionResult dans data()
    this.$router.push({
      name: 'PredictionGraphs',
      query: { result: JSON.stringify(trainResponse.data) }
    });

  } catch (error) {
    console.error(this.$t('testprediction_error_submit'), error);
  }
}
},
};
</script>

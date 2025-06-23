<template>
  <div>
    <h1>Données mortalité US (paginées)</h1>
    <ul>
      <li v-for="item in usData" :key="item.id">
         Pays : {{ item.nom_pays || item.id_pays }} | Année : {{ item.annee }} | Valeur : {{ item.valeur }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchUSMortalite } from "../../services/api.js";

const usData = ref([]);

onMounted(async () => {
  usData.value = await fetchUSMortalite(0, 25);
  console.log("usData :", usData.value);
});
</script>
import { defineStore } from 'pinia';

export const usePredictionStore = defineStore('prediction', {
  state: () => ({
    result: null,
  }),
  actions: {
    setResult(data) {
      this.result = data;
    },
    clearResult() {
      this.result = null;
    }
  }
});
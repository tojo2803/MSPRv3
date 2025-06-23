<template>
    <div>
      <h1>Données depuis l'API</h1>
      <ul>
        <li v-for="item in items" :key="item.id">{{ item.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import apiClient from '../services/api.js';
  
  export default {
    data() {
      return {
        items: [],
      };
    },
    async created() {
      try {
        const response = await apiClient.get('/'); // Remplace "/endpoint" par ton chemin d'API.
        this.items = response.data;
      } catch (error) {
        console.error('Erreur:', error);
      }
    },
  };
  </script>
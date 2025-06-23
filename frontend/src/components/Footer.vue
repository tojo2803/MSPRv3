<!-- src/components/footer.vue -->
<template>
    <footer class="footer">
      <p>&copy; 2025 {{ $t('footer_title') }}. {{ $t('footer_rights') }}</p>
      <a href="#" @click.prevent="showRGPD = true">Gérer mes cookies</a>
      <a href="/confidentialite">Politique de confidentialité</a>
    </footer>
  </template>
  
  <script>
  export default {
    name: "Footer",
  };
  </script>
  
  <style scoped>
  .footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 10px;
    position: fixed;
    bottom: 0;
    width: 100%;
  }
  </style>
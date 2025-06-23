<template>
  <div class="min-h-screen bg-gray-100">
    <Header />
    <div class="container mx-auto px-4 py-8">
      <!-- Utilisation du router-view pour afficher les vues associées aux routes -->
      <RGPDConsent />
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import RGPDConsent from "./components/RGPDConsent.vue";

export default {
  components: {
    Header,
    Footer,
    RGPDConsent,
  }
};
</script>

<style scoped>

</style>
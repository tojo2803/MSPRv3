<template>
  <div v-if="show" class="rgpd-banner">
    Ce site utilise des cookies pour améliorer votre expérience et réaliser des statistiques anonymes.
    <button @click="accept">Accepter</button>
    <button @click="decline">Refuser</button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const show = ref(false);

// Affiche le bandeau si aucun choix n'a été fait
show.value = localStorage.getItem("rgpdConsent") === null;

function accept() {
  localStorage.setItem("rgpdConsent", "accepted");
  show.value = false;
  loadAnalytics();
}

function decline() {
  localStorage.setItem("rgpdConsent", "declined");
  show.value = false;
}

function loadAnalytics() {
  if (!window.gtag) {
    const script = document.createElement("script");
    script.src = "https://www.googletagmanager.com/gtag/js?id=UA-XXXXXXX-X";
    script.async = true;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){dataLayer.push(arguments);}
    window.gtag('js', new Date());
    window.gtag('config', 'UA-XXXXXXX-X');
  }
}

// Charge analytics si déjà accepté
if (localStorage.getItem("rgpdConsent") === "accepted") {
  loadAnalytics();
}

// Permet d'afficher le bandeau depuis le footer
window.showRGPDConsent = () => { show.value = true; };
</script>

<style scoped>
.rgpd-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #222;
  color: #fff;
  padding: 1em;
  text-align: center;
  z-index: 1000;
}
.rgpd-banner button {
  margin: 0 0.5em;
}
</style>
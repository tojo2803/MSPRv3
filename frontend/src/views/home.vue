<!-- src/views/home.vue -->
<template>
    <div class="home">
      <h1>{{ $t('welcome') }}</h1>
    <p>{{ $t('home_description') }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "Home",
  };
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    margin-top: 50px;
  }
  </style>
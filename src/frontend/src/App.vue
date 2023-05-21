<template>
  <link href="https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css" rel="stylesheet">

  <MainPage url="http://localhost:5000" />
</template>

<script>
import MainPage from './components/MainPage.vue'

export default {
  name: 'App',
  components: {
    MainPage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #0d8a6b;
  margin-top: 60px;
}
</style>

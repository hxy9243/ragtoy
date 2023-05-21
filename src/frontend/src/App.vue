<template>
  <DocumentList url="http://localhost:5000" />
</template>

<script>
import DocumentList from './components/DocumentList.vue'

export default {
  name: 'App',
  components: {
    DocumentList
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

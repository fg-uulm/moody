<template>
  <div id="app">
    <LiveView msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
import LiveView from "./components/LiveView.vue";

export default {
  name: "app",
  components: {
    LiveView
  }
};
</script>

<style lang="scss">

body {
  margin:0px;
  overflow: hidden;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>

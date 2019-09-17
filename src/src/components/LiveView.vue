<template>
  <div class="liveview">
    <vue-splitter-v>
      <template slot="left">
        <img src="http://192.168.1.115:8082/stream.mjpg" class="preview" />
      </template>
      <template slot="right">
        <img src="http://192.168.1.115:8080/stream.mjpg" class="preview" />
      </template>
    </vue-splitter-v>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.VueSplitter-Handle-item {
  background-color: green;
  border: 1px solid red;
  height: 100vh;
}

</style>

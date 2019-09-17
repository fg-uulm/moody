<template>
  <div class="liveview">
    <vue-splitter-v x-class="lvsplitter">
      <template slot="left">
        <div class="pane left">
          <img src="http://192.168.1.115:8097/stream.mjpg" class="preview rot90deg" />
        </div>
      </template>
      <template slot="right" class="right">
        <div class="pane right">
          <img src="http://192.168.1.115:8098/stream.mjpg" class="preview" />
        </div>
      </template>
    </vue-splitter-v>
  </div>
</template>

<script>
export default {
  name: "LiveView",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.lvsplitter {
  background-color: green;
  border: 1px solid yellow;
  height: 100vh !important;
}

.preview {
  width: 100%;
  height: 100vh;
  object-fit: contain;
}

.rot90deg {
  transform: rotate(90deg);
}

.pane {
  height: 100%;
}

.pane.left {
  background-color: grey;
}

.pane.right {
  background-color: darkgrey;
}

</style>

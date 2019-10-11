<template>
  <b-container fluid class="main-container">
    <b-row>
      <splitpanes class="default-theme h-100">
        <pane>
          <div>
            <img src="https://dummyimage.com/720x1280/000/fff&text=Cam+SLR" />
          </div>          
        </pane>
        <pane>
          <div>
            <img src="https://dummyimage.com/720x1280/000/fff&text=Cam+Ceiling" />
          </div>
        </pane>        
      </splitpanes>
    </b-row>
  </b-container>
</template>

<script>
  // In your VueJS component.
  import { Splitpanes, Pane } from 'splitpanes'
  import 'splitpanes/dist/splitpanes.css'

  export default {
    components: { Splitpanes, Pane },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.main-container {
}
.row .nav-col {
  text-align: left;
  margin:0;
  padding:0;
}
</style>
<template>
  <b-container fluid class="main-container vh-100">
    <b-row>
      <splitpanes class="default-theme vh-100">
        <pane class="pane">
          <div class="vh-100">
            <img src="https://dummyimage.com/720x1280/000/fff&text=Cam+SLR" class="contain" id="camslr" />
          </div>          
        </pane>
        <pane class="pane">
          <div class="vh-100">
            <img src="https://dummyimage.com/720x1280/000/fff&text=Cam+Ceiling" class="contain" id="camceiling" />
          </div>
        </pane>
        <pane class="pane">
          <div class="vh-100">
            <img src="https://dummyimage.com/720x1280/000/fff&text=Cam+Outdoor" class="contain" id="camoutdoor" />
          </div>
        </pane>        
      </splitpanes>
    </b-row>
  </b-container>
</template>

<script>
  import { Splitpanes, Pane } from 'splitpanes'
  import 'splitpanes/dist/splitpanes.css'

  import io from 'socket.io-client';

  export default {
    components: { 
      Splitpanes, Pane 
    },
    created: function () {
      console.log("Created");
    },
    data: () => ({
      //socket: io(require("os").hostname()+':3001')    
      socket: io('192.168.2.192:8099')
    }),
    mounted() {
      this.socket.on('camlist', (data) => {
          console.log(data);
      });
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.main-container {
  overflow-y: hidden;
}
.main-container .pane {
  background-color: black !important;
}
.contain {
  object-fit: contain;
  max-width:100%;
  max-height:100%;
}
.row .nav-col {
  text-align: left;
  margin:0;
  padding:0;
}
</style>
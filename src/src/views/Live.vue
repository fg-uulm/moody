<template>
  <b-container fluid class="main-container vh-100">
    <b-row>
      <splitpanes class="default-theme vh-100">
        <pane size=40 min-size="10" class="pane">
          <div class="vh-100">
            <img v-bind:src="slr_src" class="contain" id="camslr" style="transform:rotate(90deg) scale(1.9);" />
          </div>          
        </pane>
        <pane size=30 class="pane">
          <div class="vh-100">
            <img v-bind:src="ceiling_src" class="contain" id="camceiling" />
          </div>
        </pane>
        <pane size=30 class="pane">
          <div class="vh-100">
            <img v-bind:src="outdoor_src" class="contain" id="camoutdoor" />
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
      socket: io('192.168.2.192:8099'),
      slr_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+SLR",
      ceiling_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+Ceiling",
      outdoor_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+Outdoor"
    }),
    mounted() {
      this.socket.on('CLIENT_LIST', (data) => {
          console.log(data);
          for (var i = data.length - 1; i >= 0; i--) {
            if(data[i].type != undefined && data[i].type == "camceiling") {
                this.ceiling_src = "http://"+data[i].address+":8098/stream.mjpg";
            } else if(data[i].type != undefined && data[i].type == "camslr") {
                this.slr_src = "http://"+data[i].address+":8097/stream.mjpg";
            } else if(data[i].type != undefined && data[i].type == "camoutdoor") {
                this.outdoor_src = "http://"+data[i].address+":8096/stream.mjpg";
            }
          }
      });
      this.socket.emit('REGISTER_CLIENT', 'uilive');
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
  object-fit: fill;
  max-width:100%;
  max-height:100%;
}
.row .nav-col {
  text-align: left;
  margin:0;
  padding:0;
}
</style>
<template>
  <b-container fluid class="main-container vh-100">
    <b-row>
      <splitpanes class="default-theme vh-100">
        <pane size=40 min-size="10" class="pane">
          <div class="vh-100">
            <img v-bind:src="slr_src" class="contain" id="camslr" />
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
    <b-row class="keystate_overlay">
      <b-col cols="12">
        <div v-if="pttPressed">MIC ON</div>
      </b-col>
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
      window.addEventListener('keydown', this.onkeydown);
      window.addEventListener('keyup', this.onkeyup);
    },
    data: () => ({
      //socket: io(require("os").hostname()+':8099'), 
      socket: io('10.0.0.25:8099'),
      slr_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+SLR",
      ceiling_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+Ceiling",
      outdoor_src: "https://dummyimage.com/720x1280/004/fff&text=Cam+Outdoor",
      pttPressed: false

    }),
    methods: {
      onkeydown(event){
        //this.socket.emit('KEYB_INPUT', 10);
        console.log(event);
        if(event.code == "Space") {
          if(!this.pttPressed) {
            this.pttPressed = true;
            this.socket.emit("broadcast", {method:"ptt",payload:"120"}); 
          }
        }        
      },
      onkeyup(event){
        //this.socket.emit('KEYB_INPUT', 10);
        console.log(event);
        if(event.code == "Space") {
          this.pttPressed = false;
          this.socket.emit("broadcast", {method:"ptt",payload:"0"}); 
        } else if(event.code == "Enter") {
          this.socket.emit("takepicture","");
        }  else if(event.code == "Tab") {
          this.socket.emit("broadcast", {method:"pttAgain",payload:"true"}); 
        }
      },
    },
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
.keystate_overlay {
  width: 100%;
  position: absolute;
  bottom:0;
  left:0;
  color:red;
  font-size: 60pt;
  background-color: rgba(0,0,0,0.2);
}
</style>
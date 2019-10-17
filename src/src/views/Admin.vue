<template>
    <b-container fluid class="main-container">
        <b-row>
            <b-col cols="8" class="text-left">
                <h2>Log</h2>
                <b-form-textarea
                  id="textarea-rows"
                  placeholder="Log textarea"
                  rows="30"
                  :value="logsAcc"
                  disabled
                  >            
                  </b-form-textarea>
            </b-col>
            <b-col cols="4" class="text-left">
                <h2>Send cmds</h2>
            </b-col>
        </b-row>
    </b-container>
</template>


<script>
  import io from 'socket.io-client'; 

  export default {
    components: { 

    },
    created: function () {

    },
    data: () => ({
      //socket: io(require("os").hostname()+':8099'), 
      socket: io('10.0.0.25:8099'),
      logsAcc: new Date().toLocaleTimeString()+" | --- Logging start ---\n", 
    }),
    methods: {
      sendCmd(cmd, payload) {
        console.log("Send Cmd: "+cmd+" |||| Payload: "+payload);
        this.socket.emit(cmd, payload); 
      },
      broadcastCmd(cmd, payloadIn) {
        console.log("broadcast Cmd: "+cmd+" |||| Payload: "+payloadIn);
        this.socket.emit("broadcast", {method:cmd,payload:payloadIn}); 
      },      
    },
    mounted() {      
      //SIO handlers
      this.socket.on('CLIENT_LIST', (data) => {
        console.log(data);          
      });
      this.socket.on('log', (data) => {        
        this.logsAcc += new Date().toLocaleTimeString()+" | "+JSON.stringify(data, null)+"\n";
        //console.log("New log line: "+JSON.stringify(data));
      });
      this.socket.emit('REGISTER_CLIENT', 'uiadmin');
    }
  }
</script>


<style>

@import url('https://fonts.googleapis.com/css?family=Work+Sans');

body {
  background-color: black;
  color:white;
  font-family: "Work Sans" !important;
  font-weight: 300;
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Old versions of Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Opera and Firefox */
}
.main-container {
  height:100vh;
  overflow:hidden;
}
.w-20 {
  width:20vw;
}
.h-20 {
  height: 3vh;
}
.mh-10 {
  min-height: 10vh;
}
</style>
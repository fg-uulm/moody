<template>
  <b-container fluid class="main-container">
    <b-row>
      <b-col cols="12" class="text-left">
        <span class="header text-left">Styles</span>
      </b-col>
    </b-row>
    <b-row class="previews justify-content-center" id="previews">
          <b-card-group deck :key="fullrerender">
            <b-card :class="[{ active : currentEffect == getImgID(num)},{ inactive : currentEffect != getImgID(num)}]" v-bind:img-src="tmpimg" v-for="num in numEffects" :key="num" :id="getImgID(num)" v-on:click="selectpic" img-top>
            </b-card>
          </b-card-group>
    </b-row>    
    <!---<b-row>
      <b-col cols="12" class="text-left">
        <span class="header text-left">Event Log</span>
      </b-col>
    </b-row>
    <b-row>
       <b-col>
      <b-form-textarea
      id="textarea-rows"
      placeholder="Log textarea"
      rows="8"
      disabled
      ></b-form-textarea>
       </b-col>
    </b-row>-->
    <b-row>
      <b-col class="module">
        <div class="header">Payment</div>
        <b-row>
          <b-col class="text-left work">
            <small>Inserted sum</small><br/>
            <span class="currency">{{currentSum}} Kč</span>
         </b-col>
          <b-col>
            <b-button class="h-100 w-100"  v-on:click="resetsum">Reset</b-button>
          </b-col>
        </b-row>        
      </b-col>     
      <b-col class="text-left work module" id="p1">
        <div class="header">Printer 1 (LEFT - GOLD)</div>
        <div :class="['ministatus wide' ,{ ok : p1.connected},{ notOk : p2.connected}]">Connected</div>
        <div :class="['ministatus wide' ,{ ok : p1.connected},{ notOk : p2.connected}]">OK</div>
        <div class="printerbatt">            
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p1.battlevel }]" :key="num" :id="getBattBlockID(num)" />
            <div class="battblock_label">Battery</div>
        </div>         
        <div class="printerfilm">
            <div class="battblock_label">Film</div>
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p1.filmlevel }]" :key="num" :id="getBattBlockID(num)">{{num}}</div>
        </div>
         <div class="printerprogress">
            <div class="battblock_label">Printing progress</div>
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p1.progress }]" :key="num" :id="getBattBlockID(num)" />
        </div>       
      </b-col>
      <b-col class="text-left work module" id="p2">
        <div class="header">Printer 2 (RIGHT - SILVER)</div>
        <div :class="['ministatus wide' ,{ ok : p2.connected},{ notOk : p1.connected}]">Connected</div>
        <div :class="['ministatus wide' ,{ ok : p2.connected},{ notOk : p1.connected}]">OK</div>
        <div class="printerbatt">            
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p2.battlevel }]" :key="num" :id="getBattBlockID(num)" />
            <div class="battblock_label">Battery</div>
        </div>         
        <div class="printerfilm">
            <div class="battblock_label">Film</div>
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p2.filmlevel }]" :key="num" :id="getBattBlockID(num)" >{{num}}</div>
        </div>
         <div class="printerprogress">
            <div class="battblock_label">Printing progress</div>
            <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p2.progress }]" :key="num" :id="getBattBlockID(num)" />
        </div>     
      </b-col>       
    </b-row>
     <b-row class="fixed-bottom actions module">
      <b-col>
        <b-row>
          <b-col cols="12" class="text-left">
            <span class="header text-left">Actions</span>
          </b-col>
        </b-row>
        <b-row>
          <b-button size="lg" class="mx-auto w-20 mh-10 b-critical b-red" v-on:click="ptt">PUSH TO TALK</b-button>
          <b-button size="lg" class="mx-auto w-20 mh-10 b-critical" v-on:click="pttagain">SAY AGAIN</b-button>
          <b-button size="lg" class="mx-auto w-20 mh-10 b-critical" v-on:click="snap">TAKE PICTURE</b-button>
          <b-button size="lg" class="mx-auto w-20 mh-10 b-critical b-green" v-on:click="print">PRINT CURRENT</b-button>
          <!--- lowermost row --->
        </b-row>
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
      this.effects.push("this.brightness(0)");
      this.effects.push(function(){ this.brightness(25) });
      this.effects.push(function(){ this.greyscale() });
      this.effects.push(function(){ this.colorize(25, 180, 200, 20) });
      this.effects.push(function(){ this.processKernel("Box Blur", [
          3, 1, 3,
          3, 1, 3,
          3, 1, 3
        ]) });
      this.effects.push(function(){  this.vibrance(60).hue(87).gamma(1.3).clip(7).contrast(31).saturation(62).sepia(83).noise(5) });
      
      //Initial FX / conversion to canvas      
      window.Caman("#img1 img", function(){ this.brightness(0)});
      window.Caman("#img2 img", function(){ this.brightness(0)});
      window.Caman("#img3 img", function(){ this.brightness(0)});
      window.Caman("#img4 img", function(){ this.brightness(0)});
      window.Caman("#img5 img", function(){ this.brightness(0)});
      window.Caman("#img6 img", function(){ this.brightness(0)});
      window.Caman("#img7 img", function(){ this.brightness(0)});
      console.log("Created ran again");
    },
    data: () => ({
      socket: io('192.168.2.192:8099'),
      initialPictureSrc: "moody.png",
      numEffects: 7,
      effects: [],
      currentEffect: "",
      tmpimg: "moody.png",
      fullrerender: 0,
      currentSum: 0,
      camStatus: false,
      coinStatus: false,
      wifiStatus: false,  
      p1: {
        connected: false,
        ok: false,
        battlevel: 0,
        filmlevel: 0,
        progress: 0,
      },
      p2: {
        connected: false,
        ok: false,
        battlevel: 0,
        filmlevel: 0,
        progress: 0,
      }
    }),
    methods: {
      ptt() {
        //this.socket.emit("ptt","100");
      },
      pttagain() {
        //this.socket.emit("ptt","100");
      },
      snap() {
        this.socket.emit("takepicture","");
      },
      print() {
        var canvas = document.getElementById(this.currentEffect).getElementsByTagName('canvas')[0];
        console.log(canvas);
        var b64img = canvas.toDataURL("image/jpeg").replace("data:image/jpeg;base64,","");
        this.socket.emit("broadcast",{method:"printjob",payload:b64img});
      },
      resetsum() {
        this.currentSum = 0;
      },
      getImgID(index) {
        return "img"+index;
      },
      getBattBlockID(index) {
        return "batblock"+index;
      },
      selectpic(event) {
        this.currentEffect = event.target.parentNode.id;
      },
      updatepics() {
        //Apply effects
        console.log("Onload fired");
        var targets = document.getElementById('previews').getElementsByTagName('canvas');
        for (var i = targets.length - 1; i >= 0; i--) {
          targets[i].getContext("2d").drawImage(this.tmpimg, 0,0);
        }

        //setTimeout(this.applyFX, 2000);         
      },
      applyFX() {
        console.log("applyFX");
        window.Caman.Store.items = {};
        window.Caman("#img1 img", this.tmpimg, function(){ this.brightness(0).render() });
        window.Caman("#img2 img", this.tmpimg, function(){ this.brightness(25).render() });
        window.Caman("#img3 img", this.tmpimg, function(){ this.greyscale().render() });
        window.Caman("#img4 img", this.tmpimg, function(){ this.colorize(25, 180, 200, 20).render() });
        window.Caman("#img5 img", this.tmpimg, function(){ this.processKernel("Box Blur", [
          3, 1, 3,
          3, 1, 3,
          3, 1, 3
        ]).render() });     
        window.Caman("#img6 img", function(){ this.vibrance(60).hue(87).gamma(1.3).clip(7).contrast(31).saturation(62).sepia(83).noise(5).render() });
        window.Caman("#img7 img", function(){ this.brightness(0).render() });
      },
    },
    mounted() {      
      //SIO handlers
      this.socket.on('CLIENT_LIST', (data) => {
        console.log(data);          
      });
      this.socket.on('picturedownloaded', (data) => {        
        //Conversion
        console.log("Received new shot, converting...")
        this.tmpimg = "data:image/jpeg;base64,"+data;
        this.$forceUpdate();
        this.fullrerender++;
        this.applyFX();
      });
      this.socket.on('coin', (data) => {
          var coinval = parseFloat(data);
          this.currentSum += coinval;
      });
      this.socket.on('printer_connected', (data) => {
          console.log("Printer connected: "+data);
          if(data == "gold") {
            this.p1.connected = true;
            this.p2.connected = false;
          } else if(data == "silver") {
            this.p1.connected = false;
            this.p2.connected = true;
          } else {
            this.p1.connected = false;
            this.p2.connected = false;
          }
      });
      this.socket.on('printer_status', (data) => {
          data = JSON.parse(data);
          console.log("Printer status: "+data["battery"]+" ("+this.p1.connected+","+this.p2.connected+")");
          var target = null;
          if(this.p1.connected) target = this.p1;
          else if(this.p2.connected) target = this.p2;  
            
          target.battlevel = data.battery;
          if(data.printCount > 10) {
            target.filmlevel = 0;
            target.ok = false;
          }
          else {
            target.filmlevel = data.printCount;
            target.ok = true;
          }
      });
      this.socket.on('camera_status', (data) => {
          var lines = data.split("\\n");
          var bat = lines.slice(-2)[0].slice(-4);
          console.log("Cam status: "+bat);
          if(bat === "(75)") this.camStatus = true;
          else this.camStatus = false;
      });
      this.socket.emit('REGISTER_CLIENT', 'uicontrol');
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
.b-critical {
  background-color: #cc9933;
  font-size: 2em;
  font-family: "Work Sans";
}
.b-red {
  background-color: #aa3333;
}
.b-green {
  background-color: #337733;
}
.card {
  width:200px;
  height: 340px;
  border: 3px solid rgba(0,0,0,0);
}
.previews {
  border-bottom:1px solid black;
  padding-bottom: 40px;
  padding-top: 40px;
  margin-left: 0px;
  margin-right: 0px;
}
.header {
  font-weight: 100;
  font-size: 0.8em;
  font-family: "Work Sans";
  border-bottom: 1px solid #666666;
  min-width: 107%;
  text-align: left;
  margin:0px;
  margin-bottom: 20px;
  margin-left:-15px;
  display:block;
  background-color: #333333;
  color:#999999;
  padding-left:10px;
  border-left: 40px solid #666666;
}
.ministatus {
  font-family: "Work Sans";
  border-left: 40px solid gray;
  margin:6px;
  padding-left: 10px;
  height:20px;
}
.ministatus.ok {
  border-color:  green;
}
.ministatus.notOk {
  border-color: red;
}
.ministatus.warn {
  border-color: orange;
}
.ministatus.wide {
  border-left-width: 20px;
  display: inline-block;
}
.active {
  border:3px solid #ffcccc;
}
.inactive {
  opacity: 0.3; 
}
.currency {
  font-size: 2.5em;
  color: #efefef;
}
.work {
  font-family: "Work Sans";
}
.actions {
  margin-bottom: 20px;
  margin-left:0px;
  margin-right:0px;
}
.actions .header {
  margin-left:-30px;
  min-width:103.2%; 
}
.battblock {
  width: 32px;
  height: 45px;
  background-color: #443333;
  display:inline-block;
  margin-right:5px;
  margin-left: 5px;
}
.battblock_label {
  margin-left: 5px;
  vertical-align: top;
}
.printerbatt .battblock {
  width: 10px;
  height: 20px;
  margin-right:2px;
  margin-left: 2px;
}
.printerbatt {
  display: inline-block;
  float:right;
  margin-top: 6px;
}
.printerprogress .battblock {
  height:5px;
}
.printerbatt .battblock_label {
  display: inline-block;
}
.printerfilm {
  margin-top: 15px;
}
.module  {
  background-color: #111111;
  margin: 13px;
  padding: 15px;
  padding-top:0px;
  padding-bottom: 15px;
}
.filled {
  background-color: #ccffcc;
}
</style>
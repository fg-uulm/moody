<template>
  <b-container fluid class="main-container">
    <b-row>
      <b-col cols="12" class="text-left">
        <span class="header text-left">Styles</span>
      </b-col>
    </b-row>
    <b-row class="previews justify-content-center">
          <b-card-group deck>
            <b-card :class="[{ active : currentEffect == getImgID(num)},{ inactive : currentEffect != getImgID(num)}]" v-bind:img-src="currentPictureSrc" v-for="num in numEffects" :key="num" :id="getImgID(num)" v-on:click="selectpic" img-top>
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
      <b-col>
        <div class="header">Payment</div>
        <b-row>
          <b-col class="text-left work">
            <small>Inserted sum</small><br/>
            <span class="currency">{{currentSum}} Kč</span>
         </b-col>
          <b-col>
            <b-button class="h-100 w-100">Reset</b-button>
          </b-col>
        </b-row>        
      </b-col>     
      <b-col class="text-left work" id="p2">
        <div class="header">Printer 1 (LEFT - GOLD)</div>
        <div :class="['ministatus wide' ,{ ok : p1Connected},{ notOk : p2Connected}]">Connected</div>
        <div :class="['ministatus wide' ,{ ok : p1Connected},{ notOk : p2Connected}]">OK</div>
        <div class="printerbatt">            
            <div v-for="num in 10" class="battblock" :key="num" :id="getBattBlockID(num)" />
            <div class="battblock_label">Battery</div>
        </div>        
        <div class="printerfilm">
            <div class="battblock_label">Film</div>
            <div v-for="num in 10" class="battblock" :key="num" :id="getBattBlockID(num)" />
        </div>
      </b-col>
      <b-col class="text-left work" id="p1">
        <div class="header">Printer 2 (RIGHT - SILVER)</div>
        <div :class="['ministatus wide' ,{ ok : p2Connected},{ notOk : p1Connected}]">Connected</div>
        <div :class="['ministatus wide' ,{ ok : p2Connected},{ notOk : p1Connected}]">OK</div>
        <div class="printerbatt">            
            <div v-for="num in 10" class="battblock" :key="num" :id="getBattBlockID(num)" />
            <div class="battblock_label">Battery</div>
        </div>        
        <div class="printerfilm">
            <div class="battblock_label">Film</div>
            <div v-for="num in 10" class="battblock" :key="num" :id="getBattBlockID(num)" />
        </div>
      </b-col>
       <b-col class="text-left work">
        <div class="header">Services</div>
        <div :class="['ministatus' ,{ ok : camStatus},{ notOk : !camStatus}]">Camera</div>
        <div :class="['ministatus' ,{ ok : coinStatus},{ notOk : !coinStatus}]">Coins</div>
        <div :class="['ministatus' ,{ ok : wifiStatus},{ notOk : !wifiStatus}]">Wifi</div>        
      </b-col>
    </b-row>
     <b-row class="fixed-bottom actions">
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
      this.effects.push(function(){ this.brightness(25).render(); });
      this.effects.push(function(){ this.greyscale().render(); });
      this.effects.push(function(){ this.colorize(25, 180, 200, 20).render(); });
      this.effects.push(function(){ this.processKernel("Box Blur", [
          3, 1, 3,
          3, 1, 3,
          3, 1, 3
        ]).render(); });
      this.effects.push(function(){  this.vibrance(60).hue(87).gamma(0.4).clip(7).contrast(31).saturation(62).sepia(83).noise(5).render(); });
      //Initial FX      
      window.Caman("#img1 img", this.effects[0]);
      window.Caman("#img2 img", this.effects[1]);
      window.Caman("#img3 img", this.effects[2]);
      window.Caman("#img4 img", this.effects[3]);
      window.Caman("#img5 img", this.effects[4]);       
    },
    data: () => ({
      socket: io('192.168.2.192:8099'),
      currentPictureSrc: "https://dummyimage.com/300x450/300/fff&text=Style",
      numEffects: 7,
      effects: [],
      currentEffect: "",
      currentSum: 0,
      camStatus: false,
      coinStatus: false,
      wifiStatus: false,  
      p1Connected: false,
      p2Connected:true,    
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
      getImgID(index) {
        return "img"+index;
      },
      getBattBlockID(index) {
        return "batblock"+index;
      },
      selectpic(event) {
        console.log(event.target.parentNode.id);
        this.currentEffect = event.target.parentNode.id;
      }
    },
    mounted() {      
      //SIO handlers
      this.socket.on('CLIENT_LIST', (data) => {
        console.log(data);          
      });
      this.socket.on('picturedownloaded', (data) => {
        this.numEffects = 0;
        this.currentPictureSrc = "data:image/jpeg;base64,"+data;
        this.numEffects = 7;
        //Apply effects
        window.Caman("#img1 canvas", this.effects[0]);
        window.Caman("#img2 canvas", this.effects[1]);
        window.Caman("#img3 canvas", this.effects[2]);
        window.Caman("#img4 canvas", this.effects[3]);
        window.Caman("#img5 canvas", this.effects[4]);       
      });
      this.socket.on('printer_status', (data) => {
          console.log(data);
      });
      this.socket.on('coin', (data) => {
          console.log(data);
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
  background-color: #ee6600;
  font-size: 2em;
  font-family: "Work Sans";
}
.b-red {
  background-color: #ee0200;
}
.b-green {
  background-color: #007700;
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
  border-bottom: 1px solid white;
  min-width: 100%;
  text-align: left;
  margin-bottom: 20px;
  margin-top:40px;
  display:inline-block;
  background-color: #333333;
  color:white;
  padding-left:10px;
  border-left: 40px solid white;
}
.ministatus {
  font-family: "Work Sans";
  border-left: 40px solid gray;
  margin:6px;
  padding-left: 10px;
  height:20px;
}
.ministatus.ok {
  border-left: 40px solid green;
}
.ministatus.notOk {
  border-left: 40px solid red;
}
.ministatus.warn {
  border-left: 40px solid orange;
}
.ministatus.wide {
  border-left: 20px solid;
  display: inline-block;
}
.active {
  border:3px solid #ffcccc;
  background-color: #ffcccc;
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
}
.battblock {
  width: 35px;
  height: 45px;
  background-color: gray;
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
.printerbatt .battblock_label {
  display: inline-block;
}
.printerfilm {
  margin-top: 15px;
}
</style>
<template>
  <b-container fluid class="main-container">
    <div class="overlay" v-if="!this.renderComplete">Processing...</div>
    <b-row>
      <b-col cols="12" class="text-left">
        <span class="header text-left">Styles</span>
      </b-col>
    </b-row>
    <b-row class="previews justify-content-center" id="previews">
      <b-col cols="12" class="text-left">  
        <b-card-group deck :key="fullrerender">
          <b-card :class="[{ active : currentEffect == getImgID(num)},{ inactive : currentEffect != getImgID(num)}]" v-bind:img-src="tmpimg" v-for="num in numEffects" :key="num" :id="getImgID(num)" v-on:click="selectpic" img-top>
          </b-card>
        </b-card-group>
      </b-col>    
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
     <b-row class="fixed-bottom" >
      <b-col>
        <b-row>
          <b-col class="module">
            <div class="header">Payment</div>
            <b-row>
              <b-col class="text-left work">
                <small>Inserted sum</small><br/>
                <span class="currency">{{currentSum}} Kč</span>
              </b-col>
              <b-col>
                <b-button class="h-100 w-100"  v-on:click="resetsum" squared >Reset</b-button>
              </b-col>
            </b-row>        
          </b-col>     
          <b-col :class="['text-left work module',{ pinactive : !p1.connected}]" id="p1" v-on:click="activatePrinter(1)">
            <div class="header">Printer 1 (LEFT - GOLD)</div>
            <div class="overlay" v-if="!p1.connected">
              <span v-if="!p1.connected && !p2.connected"><br/><br/><br/>Please wait</span>
              <span v-else><br/><br/><br/>Tap to activate</span>              
            </div>
            <div :class="['ministatus wide' ,{ ok : p1.connected},{ notOk : p2.connected}]">Con</div>
            <div :class="['ministatus wide' ,{ ok : p1.connected},{ notOk : p2.connected}]">OK</div>
            <div class="printerbatt">
              <div class="battblock_label">Batt</div>                     
              <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p1.battlevel }]" :key="num" :id="getBattBlockID(num)" />            
            </div>         
            <div class="printerfilm">
              <div class="battblock_label">Film</div>
              <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p1.filmlevel }]" :key="num" :id="getBattBlockID(num)">{{num}}</div>
            </div>
            <div class="printerprogress">
              <div class="battblock_label">Printing progress</div>
              <div v-for="num in 50" :class="['battblock' ,{ filled : num <= p1.progress }]" :key="num" :id="getBattBlockID(num)" />
            </div>       
          </b-col>
          <b-col :class="['text-left work module',{ pinactive : !p2.connected}]" id="p2" v-on:click="activatePrinter(2)">
            <div class="header">Printer 2 (RIGHT - SILVER)</div>
            <div class="overlay" v-if="!p2.connected">
              <span v-if="!p1.connected && !p2.connected"><br/><br/><br/>Please wait</span>
              <span v-else><br/><br/><br/>Tap to activate</span>              
            </div>
            <div :class="['ministatus wide' ,{ ok : p2.connected},{ notOk : p1.connected}]">Con</div>
            <div :class="['ministatus wide' ,{ ok : p2.connected},{ notOk : p1.connected}]">OK</div>
            <div class="printerbatt"> 
              <div class="battblock_label">Batt</div>         
              <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p2.battlevel }]" :key="num" :id="getBattBlockID(num)" />           
            </div>         
            <div class="printerfilm">
              <div class="battblock_label">Film</div>
              <div v-for="num in 10" :class="['battblock' ,{ filled : num <= p2.filmlevel }]" :key="num" :id="getBattBlockID(num)" >{{num}}</div>
            </div>
            <div class="printerprogress">
              <div class="battblock_label">Printing progress</div>
              <div v-for="num in 50" :class="['battblock' ,{ filled : num <= p2.progress }]" :key="num" :id="getBattBlockID(num)" />
            </div>     
          </b-col>       
        </b-row>
        <b-row class="actions module">
          <b-col>
            <b-row>
              <b-col cols="12" class="text-left">
                <span class="header text-left">Actions</span>
              </b-col>
            </b-row>
            <b-row>
              <b-button size="lg" class="mx-auto w-20 mh-10 b-critical b-red" squared v-on:touchstart="pttStart" v-on:mousedown="pttStart" v-on:touchend="pttEnd" v-on:mouseup="pttEnd">PUSH TO TALK</b-button>
              <b-button size="lg" class="mx-auto w-15 mh-10 b-critical" squared v-on:click="pttAgain">SAY AGAIN</b-button>
              <b-button size="lg" class="mx-auto w-20 mh-10 b-critical" squared v-on:click="snap">TAKE PICTURE</b-button>
              <b-button size="lg" class="mx-auto w-15 mh-10 b-critical" squared v-on:click="resetPics">RESET PICS</b-button>
              <!-- <b-button size="lg" class="mx-auto w-20 mh-10 b-critical b-green" squared v-on:click="print" :disabled="currentSum < 0.5">PRINT CURRENT</b-button> -->
              <b-button size="lg" class="mx-auto w-20 mh-10 b-critical b-green" squared v-on:click="print">PRINT CURRENT</b-button>
              <!--- lowermost row --->
            </b-row>
          </b-col>
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
      window.Caman.Filter.register("boxBlur", function () {
        // Instead of calling process, we call processKernel.
        // The first argument is an arbitrary name used to 
        // identify the filter. The optional 3rd and 4th arguments
        // are the divisor and bias, respectively.
        this.processKernel("Box Blur", [
          1, 1, 1,
          1, 1, 1,
          1, 1, 1
          ]);
      });
    },
    data: () => ({
      //socket: io(require("os").hostname()+':8099'), 
      socket: io('10.0.0.25:8099'),
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
      renderComplete: true,
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
      pttStart() {
        console.log("PTTStart");
        this.socket.emit("broadcast", {method:"ptt",payload:"120"}); 
      },
      pttEnd() {
        console.log("PTTEnd");
        this.socket.emit("broadcast", {method:"ptt",payload:"0"}); 
      },
      pttAgain() {
        this.socket.emit("broadcast", {method:"pttAgain",payload:"true"}); 
      },
      snap() {
        this.tmpimg = "moody.png";
        this.currentEffect = "none";
        this.$forceUpdate();
        this.fullrerender++;     
        this.socket.emit("takepicture","");
      },
      print() {
        var canvas = document.getElementById(this.currentEffect).getElementsByTagName('canvas')[0];
        console.log(canvas);
        var b64img = canvas.toDataURL("image/jpeg").replace("data:image/jpeg;base64,","");
        this.socket.emit("broadcast",{method:"printjob",payload:b64img});
        this.currentSum = 0;
      },
      resetsum() {
        this.currentSum = 0;
      },
      resetPics() {
        for (var i = 1; i <= this.numEffects; i++) {
          console.log("Reset img"+i);
          document.getElementById("img"+i).childNodes[0].getContext("2d").putImageData(this.imgDataStore["img"+i], 0, 0 );
        }
      },
      getImgID(index) {
        return "img"+index;
      },
      getBattBlockID(index) {
        return "batblock"+index;
      },
      selectpic(event) {
        if(this.currentEffect == event.target.parentNode.id) {          
          document.getElementById(event.target.parentNode.id).childNodes[0].getContext("2d").putImageData(this.imgDataStore[event.target.parentNode.id], 0, 0 );
          this.applyGlitch(event.target.parentNode.id);
        }
        else this.currentEffect = event.target.parentNode.id;
      },
      updatepics() {
        //Apply effects
        console.log("Onload fired");
        /*var targets = document.getElementById('previews').getElementsByTagName('canvas');
        for (var i = targets.length - 1; i >= 0; i--) {
          targets[i].getContext("2d").drawImage(this.tmpimg, 0,0);
        }*/     
      },
      applyFX() {
        console.log("applyFX");
        window.Caman.Store.items = {};
        var that = this; //oh wow, this hurts (or that?)
        window.Caman("#img1 img", this.tmpimg, function(){ this.render(console.log("FX1 complete")) });
        window.Caman("#img2 img", this.tmpimg, function(){ this.greyscale().render(console.log("FX2 complete")) });
        window.Caman("#img3 img", this.tmpimg, function(){ this.colorize(50, 40, 250, 20).render(console.log("FX3 complete")) });
        window.Caman("#img4 img", this.tmpimg, function(){ this.stackBlur().render(console.log("FX4 complete")) });     
        window.Caman("#img5 img", function(){ this.sepia(83).noise(5).render(that.renderCompleteCallback)});
        window.Caman("#img6 img", this.tmpimg, function(){ this.render() });
        window.Caman("#img7 img", this.tmpimg, function(){ this.render() });     
      },
      applyGlitch(target) {
        console.log("applyGlitch on "+target);
        //var that = this; //slowly, I'm getting used to this...
        var canvas = document.getElementById(target).childNodes[0];
        var ctx = canvas.getContext("2d");
        var imageData = ctx.getImageData( 0, 0, canvas.width, canvas.height );
        var rndSeed = Math.random()*100;

        window.glitch( { seed: rndSeed, quality: 90, amount: 11, iterations: 13 } )
        .fromImageData( imageData ) 
        .toImageData()
        .then( function( imageData ) {              
              //that.tmpimg = dataURL;
              //imgNode.src = dataURL;
              ctx.putImageData( imageData, 0, 0 );
            } 
            );
      },
      activatePrinter(id) {
        this.p1.connected = false;
        this.p2.connected = false;
        if(id == 1) this.socket.emit("broadcast",{method:"wificonnect",payload:"gold"});
        else if(id == 2) this.socket.emit("broadcast",{method:"wificonnect",payload:"silver"});
      },
      renderCompleteCallback() {
        console.log("FX render complete");
        this.renderComplete = true;
        this.currentEffect = "img1";
        console.log("Save original image data");
        this.imgDataStore = {
          "img1": document.getElementById("img1").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img2": document.getElementById("img2").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img3": document.getElementById("img3").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img4": document.getElementById("img4").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img5": document.getElementById("img5").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img6": document.getElementById("img6").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
          "img7": document.getElementById("img7").childNodes[0].getContext("2d").getImageData( 0, 0, 600, 900 ),
        }
        //this.applyGlitch("img1");
      },
    },
    mounted() {      
      //SIO handlers
      this.socket.on('CLIENT_LIST', (data) => {
        console.log(data);          
      });
      this.socket.on('picturedownloaded', (data) => {        
        //Conversion
        this.renderComplete = false;
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
      this.socket.on('print_progress', (data) => {
        console.log("Progress: "+data);
        var target = null;
        if(this.p1.connected) target = this.p1;
        else if(this.p2.connected) target = this.p2;  

        target.progress = Math.round(data.percent/2);
      });
      this.socket.on('print_success', (data) => {
        console.log("Print success "+data);
        var target = null;
        if(this.p1.connected) target = this.p1;
        else if(this.p2.connected) target = this.p2;  

        target.progress = 0;
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

          .w-15 {
            width:15vw;
          }

          .h-20 {
            height: 3vh;
          }
          .mh-10 {
            min-height: 10vh;
          }
          .b-critical {
            background-color: #cc9933;
            font-size: 1.3em;
            font-family: "Work Sans";
          }
          .b-red {
            background-color: #aa3333;
          }
          .b-green {
            background-color: #337733;
          }
          .card-deck {
            overflow-x: auto;
            overflow-y: hidden;
            max-height:50vh;
            height:50vh;
            display:-webkit-box;
          }
          .card-deck .card {
            max-height: 50vh;
            border: 3px solid rgba(0,0,0,0);
            margin-right:5px;
            margin-left:5px;
            min-width: 200px;
            height:50vh;
          }
          .card-img-top {
            max-width: 100%;
            max-height: 100%;
          }
          .previews {
            border-bottom:1px solid black;
            padding-bottom: 5px;
            padding-top: 5px;
            margin-left: 0px;
            margin-right: 0px;
          }
          .header {
            font-weight: 100;
            font-size: 0.8em;
            font-family: "Work Sans";
            border-bottom: 1px solid #666666;
            min-width: 100%;
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
            width: 8%;
            height: 33px;
            background-color: #443333;
            display:inline-block;
            margin-right:1%;
            margin-left: 1%;
          }
          .battblock_label {
            margin-left: 1px;
            margin-right:5px;
            vertical-align: top;
          }
          .printerbatt .battblock {
            width: 2%;
            height: 20px;
            margin-right:2px;
            margin-left: 2px;
          }
          .printerbatt {
            display: block;
            float:right;
            margin-top: 8px;
            width: 35%;
          }
          .printerprogress .battblock {
            height:5px;
            width:1.6%;
            margin-left: 0px;
            margin-right: 1px;
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
          .pinactive {
            opacity: 0.5;
          }
          .overlay {
            display: block;
            background-color: rgba(0,0,0,0.4);
            width:100%;
            height:100%;
            position:absolute;
            top:0;
            left:0;
            color:white;
            font-size: 18pt;
            margin: auto;
            text-align: center;
            vertical-align: middle;
            z-index: 9999;
          }
          .pinactive .overlay {
            display: block;
            width:100%;
            height:100%;
            position:absolute;
            top:0;
            left:0;
            color:white;
            font-size: 18pt;
            margin: auto;
            text-align: center;
            vertical-align: middle;
          }
        </style>
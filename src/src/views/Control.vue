<template>
  <b-container fluid class="main-container">
    <b-row>
      <b-col cols="12" class="text-left">
        <span class="header text-left">Styles</span>
      </b-col>
    </b-row>
    <b-row class="previews justify-content-center">
          <b-card-group deck>
            <b-card :class="[{ active : currentEffect == getID(num)},{ inactive : currentEffect != getID(num)}]" v-bind:img-src="currentPictureSrc" v-for="num in numEffects" :key="num" :id="getID(num)" v-on:click="selectpic" img-top>
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
      <b-col class="text-left work">
        <div class="header">Camera</div>
        Info on Camera<br/>
        Second Line<br/>
        Third line<br/>
      </b-col>
      <b-col class="text-left work">
        <div class="header">Printer 1</div>
        Info on Printer 1 of 2<br/>
        Second Line<br/>
        Third line<br/>
      </b-col>
      <b-col class="text-left work">
        <div class="header">Printer 2</div>
        Info on Printer 1 of 2<br/>
        Second Line<br/>
        Third line<br/>
      </b-col>
    </b-row>
    
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
  </b-container>
</template>

<script>
  import io from 'socket.io-client'; 

  export default {
    components: { 

    },
    created: function () {
      //nothing
    },
    data: () => ({
      socket: io('192.168.2.192:8099'),
      currentPictureSrc: "https://dummyimage.com/300x450/300/fff&text=Style",
      numEffects: 7,
      currentEffect: "",
      currentSum: 0,
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
        var canvas = document.getElementById(this.currentEffect).getElementsByTagName('canvas')[0];;
        console.log(canvas);
        var b64img = canvas.toDataURL("image/jpeg").replace("data:image/jpeg;base64,","");
        this.socket.emit("broadcast",{method:"printjob",payload:b64img});
      },
      getID(index) {
        return "img"+index;
      },
      selectpic(event) {
        console.log(event.target.parentNode.id);
        this.currentEffect = event.target.parentNode.id;
      }
    },
    mounted() {
      this.socket.on('CLIENT_LIST', (data) => {
        console.log(data);          
      });
      this.socket.on('picturedownloaded', (data) => {
        this.numEffects = 0;
        console.log("Received pic data");
        this.currentPictureSrc = "data:image/jpeg;base64,"+data;
        this.numEffects = 7;
        //Apply effects
        window.Caman("#img1 img", function () {
          this.brightness(25).render();
        });
        window.Caman("#img2 img", function () {
          this.greyscale().render();
        });
        window.Caman("#img3 img", function () {
          this.colorize(25, 180, 200, 20).render();
        });
        window.Caman("#img4 img", function () {
          this.processKernel("Box Blur", [
            3, 1, 3,
            3, 1, 3,
            3, 1, 3
          ]).render();
        });
        window.Caman("#img5 img", function () {
          this.vibrance(60).hue(87).gamma(0.4).clip(7).contrast(31).saturation(62).sepia(83).noise(5).render();
        });
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
</style>
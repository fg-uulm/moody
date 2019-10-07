const mumble = require('mumble');
const fs = require('fs');
const io = require('socket.io-client');
const DMX = require('dmx');

var artnetOptions = {
    host: '127.0.0.1'
}
 
const artnet = require('artnet')(artnetOptions);
const dmx = new DMX();
//const universe = dmx.addUniverse('demo', 'null');
var A = dmx.animation;
var universe = dmx.addUniverse('demo', 'enttec-usb-dmx-pro', '/dev/ttyUSB0') //uncomment for production

var mumbleOptions = {
    key: fs.readFileSync( 'key.pem' ),
    cert: fs.readFileSync( 'cert.pem' )
};

var masterServer = '127.0.0.1'; 
var masterServerPort = 8099;
var idleBright = 80;
var flashBright = 255;
var audioBright = 130;
var prevOnBulbs = 0;

var dmxMethod = "direct";
var flashMode = false;

/*
 * STARTUP PROCEDURES
 * ==================
 */

//Start servers
console.log( 'Connecting to socketio server' );
var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});

console.log( 'Connecting to Mumble server' );
/*mumble.connect( 'mumble://localhost', mumbleOptions, function ( error, connection ) {
    if( error ) { throw new Error( error ); }

    console.log( 'Connected' );

    connection.authenticate( 'ExampleUser' );
    connection.on( 'initialized', onInit );
    connection.on( 'voice', onVoice );
});*/

//Test artnet
artnet.set([255, 129]);

//Setup animations for direct mode
var toFlashAnim = new DMX.Animation().add({
  1: flashBright,
  2: flashBright,
  3: flashBright,
  4: flashBright,
  5: flashBright,
  6: flashBright
}, 20);

var toIdleAnim = new DMX.Animation().add({
  1: idleBright,
  2: idleBright,
  3: idleBright,
  4: idleBright,
  5: idleBright,
  6: idleBright
}, 500);

var toLevelAnim = new DMX.Animation().add({
  1: audioBright,
  2: audioBright,
  3: audioBright,
  4: audioBright,
  5: audioBright,
  6: audioBright
}, 50);

var directObj = [];


/* END STARTUP */

//SIO handlers
socket.on('connect', function(in_socket) {
    //Handle new connections, sync state
  console.log("SIO Connected: "+socket);

  //Pong method for keepalive
  socket.on('PING', function(data) {
    socket.emit('PONG', data);
    console.log("PONGing: "+data);
  });
});

socket.on('disconnect', function(in_socket) {
    console.log("SIO Disconnected");
});

socket.on('flashstart', function(brightness) {
    console.log("SIO Flashlight start");
    flashMode = true;
    //Send DMX animation for flash scene (artnet, no ani)
    if(dmxMethod == "artnet") artnet.set([flashBright,flashBright,flashBright,flashBright,flashBright,flashBright]);
    else if(dmxMethod == "direct") {
        toFlashAnim.run(universe);
    }
});

socket.on('flashend', function(brightness) {
    console.log("SIO Flashlight end");
    flashMode = false;
    //Send DMX animation flash scene end (artnet, no ani)
    if(dmxMethod == "artnet") artnet.set([idleBright,idleBright,idleBright,idleBright,idleBright,idleBright]);
    else if(dmxMethod == "direct") {
        toIdleAnim.run(universe);
    }
});

socket.on('showlevel', function(level) {
    //Are we using the bulbs as flash currently?
    if(flashMode) {
      toLevelAnim.stop();
      return;
    }

    //Determine how many bulbs should be "on" (level goes from 0-100, smoothed)
    var onBulbNum = Math.round(level*6 / 100);
    var decay = false;

    // Smooth decay
    if(onBulbNum < prevOnBulbs) {
      onBulbNum = Math.round(0.7*prevOnBulbs + 0.3*onBulbNum);
      decay = true;
    }

    //"Smoothing" a.k.a. keeping the animation refreshes down if same number
    if(onBulbNum == prevOnBulbs) return;
    prevOnBulbs = onBulbNum;    

    var artnetArr = [];
    for (var i = 0; i < 6; i++) {
        if(i < onBulbNum) {
            artnetArr[i] = audioBright;
            directObj[i] = audioBright;
            //directObj[i] = 200;
        } else {
            artnetArr[i] = idleBright;
            directObj[i] = idleBright;
        }
    }

    //Send DMX for audio level
    if(dmxMethod == "artnet") artnet.set(artnetArr);
    else if(dmxMethod == "direct") {
        toLevelAnim.stop();
        toLevelAnim = new DMX.Animation().add({
          1: directObj[0],
          2: directObj[1],
          3: directObj[2],
          4: directObj[3],
          5: directObj[4],
          6: directObj[5]
        }, 0).run(universe);

        //console.log(directObj);
        //toLevelAnim.run(universe);
    }
});

socket.on('adjustidle', function(level) {
    idleBright = level;
    toIdleAnim = new DMX.Animation().add({
      1: idleBright,
      2: idleBright,
      3: idleBright,
      4: idleBright,
      5: idleBright,
      6: idleBright
    }, 500);
    toIdleAnim.run(universe);
});


socket.on('adjustflash', function(level) {
    flashBright = level;
    toFlashAnim = new DMX.Animation().add({
      1: flashBright,
      2: flashBright,
      3: flashBright,
      4: flashBright,
      5: flashBright,
      6: flashBright
    }, 500);
});

//Mumble handlers
var onInit = function() {
    console.log( 'Mumble Connection initialized' );
};

var onVoice = function( voice ) {
    var pcmData = voice;
    //console.log(parseFloat(pcmData));
};

artnet.set([flashBright,flashBright,flashBright,flashBright,flashBright,flashBright]);
artnet.set([idleBright,idleBright,idleBright,idleBright,idleBright,idleBright]);
toIdleAnim.run(universe);
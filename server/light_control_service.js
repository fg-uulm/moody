const mumble = require('mumble');
const fs = require('fs');
const io = require('socket.io-client');
const DMX = require('dmx');

var artnetOptions = {
    host: '127.0.0.1'
}
 
const artnet = require('artnet')(artnetOptions);
const dmx = new DMX();
const universe = dmx.addUniverse('demo', 'null');
var A = dmx.animation;
//var universe = dmx.addUniverse('demo', 'enttec-open-usb-dmx', '/dev/cu.usbserial-6AVNHXS8') //uncomment for production

var mumbleOptions = {
    key: fs.readFileSync( 'key.pem' ),
    cert: fs.readFileSync( 'cert.pem' )
};

var masterServer = '127.0.0.1'; 
var masterServerPort = 8099;
var idleBright = 50;
var flashBright = 255;
var audioBright = 100;

var dmxMethod = "artnet";

/*
 * STARTUP PROCEDURES
 * ==================
 */

//Start servers
console.log( 'Connecting to socketio server' );
var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});

console.log( 'Connecting to Mumble server' );
mumble.connect( 'mumble://localhost', mumbleOptions, function ( error, connection ) {
    if( error ) { throw new Error( error ); }

    console.log( 'Connected' );

    connection.authenticate( 'ExampleUser' );
    connection.on( 'initialized', onInit );
    connection.on( 'voice', onVoice );
});

//Test artnet
artnet.set([255, 129]);

//Setup animations for direct mode
const toFlashAnim = new DMX.Animation().add({
  1: flashBright,
  2: flashBright,
  3: flashBright,
  4: flashBright,
  5: flashBright,
  6: flashBright
}, 500);

const toIdleAnim = new DMX.Animation().add({
  1: idleBright,
  2: idleBright,
  3: idleBright,
  4: idleBright,
  5: idleBright,
  6: idleBright
}, 1500);


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
    //Send DMX animation for flash scene (artnet, no ani)
    if(dmxMethod == "artnet") artnet.set([flashBright,flashBright,flashBright,flashBright,flashBright,flashBright]);
    else if(dmxMethod == "direct") {
        toFlashAnim.run(universe);
    }
});

socket.on('flashend', function(brightness) {
    console.log("SIO Flashlight end");
    //Send DMX animation flash scene end (artnet, no ani)
    if(dmxMethod == "artnet") artnet.set([idleBright,idleBright,idleBright,idleBright,idleBright,idleBright]);
    else if(dmxMethod == "direct") {
        toIdleAnim.run(universe);
    }
});

socket.on('showlevel', function(level) {
    //Determine how many bulbs should be "on" (level goes from 0-100)
    var onBulbNum = Math.round(level / 100);
    var artnetArr = [];
    var directObj = {};
    for (var i = 0; i < 8; i++) {
        if(i < onBulbNum) {
            artnetArr[i] = audioBright;
            directObj[i] = audioBright;
        } else {
            artnetArr[i] = idleBright;
            directObj[i] = idleBright;
        }
    }

    //Send DMX for audio level
    if(dmxMethod == "artnet") artnet.set(artnetArr);
    else if(dmxMethod == "direct") {
        var toLevelAnim = new DMX.Animation().add({
          1: audioBright,
          2: idleBright,
          3: idleBright,
          4: idleBright,
          5: idleBright,
          6: idleBright
        }, 100);

        toLevelAnim.run(universe);
    }
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
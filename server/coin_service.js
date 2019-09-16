//Consts
const isPi = require('detect-rpi');
const fs = require('fs');
const SerialPort = require('serialport');
const io = require('socket.io-client');

//Error types + handling
var E = {
    SYSTEM_FAILURE: 1024,
    COINDETECTOR_MISSING: 512,
    COINDETECTOR_FAULTY: 256,
}
var activeErrors = [];

//Vars
var port;
var serdev = '/dev/coin_uart';
/* This device only works if there's an udev rule creating an appropriate symlink.
See e.g. https://unix.stackexchange.com/questions/66901/how-to-bind-usb-device-under-a-static-name
The same needs to be done for olad not to lock USBserial interfaces for each other */

var errors = [];

var masterServer = '127.0.0.1'; 
var masterServerPort = 8099;

/*
 * STARTUP PROCEDURES
 * ==================
 */

//Start servers
var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});

//Pi / Win detection for serial device
if(isPi()) {
    if(fs.existsSync('/dev/ttyUSB1')) serdev = '/dev/ttyUSB1';
    console.log("RPi Mode");
} else {
    serdev = "COM3";
    console.log("Win Mode");
}

//Serial setup
port = new SerialPort(serdev, {
    baudRate: 9600
});
console.log("Using serial device "+serdev);

//Fail condition for coin detector
if(serdev == '/dev/ttyAMA0' && isPi()) {
    raiseError(E.COINDETECTOR_MISSING);
}

/* ------------- END STARTUP -------------- */



/*
* Serial port stuff
*/
port.on('data', function (data) {
  var received = data.readUIntLE(0,1);
	console.log('Serial Port Data:', received);
  console.log('Raw data:',data);
  if(!isNaN(received) && received != 0) {
    console.log("Coin inserted: "+received/10.0)
    socket.emit("coin", received/10.0);
  } 
  else {
    raiseError(E.COINDETECTOR_FAULTY);
  }
})

/*
* SIO stuff
*/
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


/*
 * Process / SIGCAPTURE stuff
 */
 process.on('SIGTERM', () => {
  console.info('SIGTERM signal received.');
  process.exit(0);
});

 process.on('SIGINT', () => {
  console.info('SIGINT signal received.');
  process.exit(0);
});

/*
 * Error handling
 */
function raiseError(errorType) {
  console.log("Raise Error of type "+errorType);
  activeErrors[errorType] = true;
  console.log("Error stack now: "+activeErrors);
  //Emit highest prioritized error
  emitError();
}

function clearError(errorType) {
  activeErrors[errorType] = false;
  console.log("Clear error of type "+errorType);
  //Emit highest prioritized error (or 0, if none left)
  emitError();
}

function emitError() {
  var highestError = 0;
  for (var i = 0; i < activeErrors.length; i++) {
    if(activeErrors[i] != undefined && activeErrors[i] == true) highestError = i; 
  }
  socket.emit("error", highestError); 
}


/*
* MAIN LOGIC
*/ 

// none, event driven so far
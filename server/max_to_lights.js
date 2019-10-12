var osc = require('osc-min');
var dgram = require('dgram');
var io = require('socket.io-client');

var remote;

var masterServer = '192.168.2.192'; 
var masterServerPort = 8099;

var lowerLimit = -70;
var upperLimit = 12;

var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});

// Map helper
function map(val, low1, high1, low2, high2) {
  return (val - low1) / (high1 - low1) * (high2 - low2) + low2;
}

//Register
socket.on('connect', function(in_socket) {
  //Handle new connections, sync state
  console.log("SIO Connected: "+socket);
  socket.emit("REGISTER_CLIENT","maxtolight");
});

// Listen for OSC messages from Max and fwd them to Moodys light control
var udp = dgram.createSocket('udp4', function(msg, rinfo) {

  // save the remote address
  remote = rinfo.address;

  try {
  	outMsg = osc.fromBuffer(msg)
    //console.log(msg);
    //Process and send to SIO
    var level = map(outMsg.args[0].value, lowerLimit, upperLimit, 0, 100);
    console.log(level);
    socket.emit("broadcast", {method:"showlevel",payload:level});
  } catch (err) {
    console.log('Could not decode OSC message');
  }

});

udp.bind(9898);
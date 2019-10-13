var OSC = require('osc-js')
var dgram = require('dgram');
var io = require('socket.io-client');

var remote;

var masterServer = '192.168.188.55'; 
var masterServerPort = 8099;

var lowerLimit = -70;
var upperLimit = 12;

var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});
var osc = new OSC({ plugin: new OSC.DatagramPlugin() })
//osc.open({ port: 9897 })

//SIO handlers
socket.on('connect', function(in_socket) {
    //Handle new connections, sync state
  console.log("SIO Connected: ");
  console.log(socket.id);

  //Pong method for keepalive
  socket.on('PING', function(data) {
    socket.emit('PONG', data);
    console.log("PONGing: "+data);
  });
});

socket.on('disconnect', function(in_socket) {
    console.log("SIO Disconnected");
});

socket.on('ptt', function(lvl) {
    console.log("SIO PTT: "+lvl);
	osc.send(new OSC.Message('/ptt', parseInt(lvl)));
});
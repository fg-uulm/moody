//server.js
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var initialConfig = {
  isDryRun : false,
  debugLevel : 5
};

var clients = [];

io.on('connection', function (socket) {
 if(initialConfig.debugLevel > 3) console.log('New connection:'+socket);

   //Send out initial config
   io.emit("initialConfig", initialConfig);

   //Regular alive / status polling
   setInterval(function(){
    socket.emit("request_status","null");
  }.bind(this), 10000);

   //Register client
   socket.on("REGISTER_CLIENT", function (clientType) {
      //clients.push({id: socket.id, type: clientType, ipv4: socket.handshake.address.replace('::ffff:', '')});
      console.log('A ' + clientType + ' registered from ' + JSON.stringify(socket.handshake.address.replace('::ffff:', '')))
      io.sockets.clients().connected[socket.id].deviceType = clientType
      io.sockets.clients().connected[socket.id].deviceAddress = socket.handshake.address.replace('::ffff:', '')
      clients = [];
      for (const clientId of Object.keys(io.sockets.clients().connected)) {
        try {
          clients.push({ id: io.sockets.clients().connected[clientId].id, type: io.sockets.clients().connected[clientId].deviceType, address: io.sockets.clients().connected[clientId].deviceAddress })              
        } catch(e) {
          console.error(clientId)
        }
      }
      io.emit("CLIENT_LIST", clients);
      io.emit('log', {method:'log', payload:"Client connected to SIO master"});
      io.emit('log', {method:'CLIENT_LIST', payload:clients});
    });

   //Socket handlers
   socket.on("disconnect", function() {
    clients = clients.filter(function( c ) {
      return c.id !== socket.id;
    });
    io.emit("CLIENT_LIST", clients);
    io.emit('log', {method:'log', payload:"Client disconnected from SIO master"});
    io.emit('log', {method:'CLIENT_LIST', payload:clients});
    console.log("Client disconnected: "+socket.id);
  });

   //Generic broadcast handler
   socket.on('broadcast', function (msg) {
    io.emit(msg.method, msg.payload);
    io.emit('log', {method:'broadcast', payload:msg});
    if(initialConfig.debugLevel > 5) console.log(msg.method, msg.payload);
  });

   //Master picture taking coordinators
   socket.on('takepicture',function(msg) {
    io.emit("flashstart", null);
    io.emit('log', {method:'flashstart', payload:""});
    setTimeout(function() {
     io.emit("capture", null);
     io.emit('log', {method:'capture', payload:""});
   }, 500);      
  });

   socket.on('captured', function(imagedata) {
    io.emit("flashend");
    io.emit('log', {method:'captured', payload:imagedata});
  });

   socket.on('picture', function(imagedata) {
    console.log("Picture received: "+imagedata.length);   	  
    io.emit('picturedownloaded', imagedata);
    io.emit('log', {method:'picture', payload:imagedata});
      //io.emit('printjob', imagedata);
    });

   socket.on('wificonnect_success', function(msg) {
    io.emit('wificonnect_success', msg);
    io.emit('log', {method:'wificonnect_success', payload:msg});
  });

   socket.on('camera_status', function(msg) {
    io.emit('camera_status', msg);
    io.emit('log', {method:'camera_status', payload:msg});
  });

   socket.on('printer_status', function(msg) {
    io.emit('printer_status', msg);
    io.emit('log', {method:'printer_status', payload:msg});
  });

   socket.on('printer_connected', function(msg) {
    io.emit('printer_connected', msg);
    io.emit('log', {method:'printer_connected', payload:msg});
  });

   socket.on('print_progress', function(msg) {
    io.emit('print_progress', msg);
    io.emit('log', {method:'print_progress', payload:msg});
  });

   socket.on('print_success', function(msg) {
    io.emit('print_success', msg);
    io.emit('log', {method:'print_success', payload:msg});
  });

   socket.on('coin', function(msg) {
    io.emit('coin', msg);
    io.emit('log', {method:'coin', payload:msg});
  });

   //Log forwarder
   socket.on('log', function(msg) {
    io.emit('log', {method:'log', payload:msg});
   });
 });

//Server startup
http.listen(8099, function () {
  console.log('listening on *:8099');
});
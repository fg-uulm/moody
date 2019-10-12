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

   //Register client
   socket.on("REGISTER_CLIENT", function (clientType) {
      console.log('A ' + msg + ' registered from ' + JSON.stringify(socket.handshake.address.replace('::ffff:', '')))
      clients.push({id: socket.id, type: clientType, ipv4: socket.handshake.address.replace('::ffff:', '')});
      console.log('A ' + msg + ' registered from ' + JSON.stringify(socket.handshake.address.replace('::ffff:', '')))
      io.sockets.clients().connected[socket.id].deviceType = msg
      io.sockets.clients().connected[socket.id].deviceAddress = socket.handshake.address.replace('::ffff:', '')
      for (const clientId of Object.keys(io.sockets.clients().connected)) {
          try {
              io.emit(
                  io.sockets.clients().connected[clientId].deviceType.toUpperCase() + '_REGISTERED',
                  { id: io.sockets.clients().connected[clientId].id, address: io.sockets.clients().connected[clientId].deviceAddress }
              )
              io.emit("CLIENT_LIST", clients);
          } catch(e) {
              console.error(clientId)
          }
      }
   });

   //Socket handlers
   socket.on("disconnect", function() {
      clients = clients.filter(function( c ) {
          return c.id !== socket.id;
      });
      console.log("Client disconnected: "+socket.id);
   });

   //Generic broadcast handler
   socket.on('broadcast', function (msg) {
      io.emit(msg.method, msg.payload);
      if(initialConfig.debugLevel > 5) console.log(msg.method, msg.payload);
   });

   //Master picture taking coordinators
   socket.on('takepicture',function(msg) {
      io.emit("flashstart", null);
      setTimeout(function() {
         io.emit("capture", null);
      }, 500);      
   });

   socket.on('picture', function(imagedata) {
   	  console.log("Picture received: "+imagedata.length);
   	  io.emit("flashend");
   	  //io.emit('picture', imagedata);
      io.emit('printjob', imagedata);
   });

   socket.on('wificonnect_success', function(msg) {
      io.emit('wificonnect_success', msg);
   });

 });

http.listen(8099, function () {
  console.log('listening on *:8099');
});
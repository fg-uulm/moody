//server.js
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

io.on('connection', function (socket) {
 console.log('New connection:'+socket);

 io.emit("PING", "1234");

   //Socket handlers
   socket.on("disconnect", () => console.log("Client disconnected: "+socket.id));

   //Generic broadcast handler
   socket.on('broadcast', function (msg) {
          io.emit(msg.method, msg.payload);
          console.log(msg.method, msg.payload);
    });

   //Master picture taking coordinators
   socket.on('takepicture',function(msg) {
      io.emit("flashstart", null);
      io.emit("capture", null);
   });

   socket.on('picture', function(imagedata) {
   	  console.log("Picture received: "+imagedata.length);
   	  io.emit("flashend");
   	  io.emit('picture', imagedata);
   })

 });

http.listen(8099, function () {
  console.log('listening on *:8099');
});
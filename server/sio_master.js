//server.js
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

io.on('connection', function (socket) {
   console.log('New connection:'+socket);
   io.emit("PING", "1234");

   //Socket handlers
   socket.on("disconnect", () => console.log("Client disconnected: "+socket.id));

   socket.on('coin', function (data) {
     console.log("Coin inserted: "+data);
   });
   
});

http.listen(8099, function () {
  console.log('listening on *:8099');
});
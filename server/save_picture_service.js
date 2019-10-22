const io = require('socket.io-client');
const fs = require('fs');

var masterServer = '10.0.0.25'; 
var masterServerPort = 8099;
var config;

var socket = io.connect('http://'+masterServer+':'+masterServerPort, { reconnect: true });

socket.on('connect', function(in_socket) {
    //Handle new connections, sync state
    console.log("SIO Connected: "+socket);
    socket.emit("REGISTER_CLIENT","picturesaver");
});

socket.on('picturedownloaded', function(data) {
    let buff = new Buffer(data, 'base64');
    let filename = "./pics/img_"+Math.floor(new Date() / 1000).toString()+".jpg"; 
    fs.writeFile(filename, buff, function(err){
        if (err) throw err
        console.log('File saved as '+filename);
    });
});

socket.on('printjob', function(data) {
    let buff = new Buffer(data, 'base64');
    let filename = "./pics/img_"+Math.floor(new Date() / 1000).toString()+".jpg"; 
    fs.writeFile(filename, buff, function(err){
        if (err) throw err
        console.log('File saved as '+filename);
    });
});
const io = require('socket.io-client');
const { spawn } = require('child_process');

arOptions = {
	channels: 2,
	rate: 16000,
	format: 'S16_LE',
	device: 'front:CARD=Mic' // find out with `arecord -L`
}

var masterServer = '127.0.0.1'; 
var masterServerPort = 8099;

var socket = io.connect('http://'+masterServer+':'+masterServerPort, {reconnect: true});

callback = function(level) {
	console.log("level: "+level);
	socket.emit("broadcast", {method:"showlevel",payload:level});
};

const arProcess = spawn('arecord', [
	'-c', arOptions.channels,
	'-r', arOptions.rate,
	'-f', arOptions.format,
	'-D', arOptions.device,
	'-V', 'mono'
], { stdio: ['ignore', 'ignore', 'pipe'] });

arProcess.stderr.on('data', function(data) {
	let level = parseInt(String(data).substr(54,2));
	if (isNaN(level)) {
		console.log(String(data))
		return;
	}
	callback(level);
});

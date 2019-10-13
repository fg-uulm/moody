const io = require('socket.io-client');
const { spawn } = require('child_process');

var masterServer = '192.168.188.55'; 
var masterServerPort = 8099;
var config;

var socket = io.connect('http://'+masterServer+':'+masterServerPort, { reconnect: true });

//Audio Level Callback
callback = function(level) {
	if(level < 0) {
		level = Math.floor(Math.random() * 100);
	}
	if(config.debugLevel > 5) console.log("level: "+level);
	socket.emit("broadcast", {method:"showlevel",payload:level});
};

socket.on('connect', function(in_socket) {
  //Handle new connections, sync state
  console.log("SIO Connected: "+socket);
  socket.emit("REGISTER_CLIENT","alsasoundlevel");
});

//Process initial global config event, setup microservice
socket.on('initialConfig', function(globalConfig) {
	config = globalConfig;
	//Runing dry, no audio input, generate random values (in callback)
	if(config.isDryRun) {
		if(config.debugLevel > 3) console.log("Running dry");		
		setInterval(callback, 100, -1)
	//Running live, using audio input from ALSA sound interface
	} else {
		if(config.debugLevel > 3) console.log("Not running dry");
		
		arOptions = {
			channels: 2,
			rate: 16000,
			format: 'S16_LE',
			device: 'front:CARD=Mic' // find out with `arecord -L`
		}		

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
				if(config.debugLevel > 3) console.log(String(data))
				return;
			}
			callback(level);
		});
	}
});






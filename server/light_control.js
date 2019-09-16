var mumble = require('mumble'),
    fs = require('fs');

var options = {
    key: fs.readFileSync( 'key.pem' ),
    cert: fs.readFileSync( 'cert.pem' )
};

console.log( 'Connecting' );
mumble.connect( 'mumble://localhost', options, function ( error, connection ) {
    if( error ) { throw new Error( error ); }

    console.log( 'Connected' );

    connection.authenticate( 'ExampleUser' );
    connection.on( 'initialized', onInit );
    connection.on( 'voice', onVoice );
});

var onInit = function() {
    console.log( 'Connection initialized' );
};

var onVoice = function( voice ) {
    var pcmData = voice;
    console.log(parseFloat(pcmData));
};
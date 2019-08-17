var http       = require("http");
var express    = require('express');
var app        = express();
var bodyParser = require('body-parser');


/*
 *  Init / Startup
 */

//start body-parser configuration
app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));
//end body-parser configuration

//enable cors
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});
//end enable cors

//create app server
var server = app.listen(3000,  "127.0.0.1", function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Moody Backend App listening at http://%s:%s", host, port)

}); 



/*
 *  Reactive Behaviours / Event Endpoints
 */

//REST-Endpoint um alle Stationen auszugeben
app.get('/status', function (req, res, next) {
	  res.end(JSON.stringify({ status : true}));
});
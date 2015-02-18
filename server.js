var os = require('os');
var cluster = require('cluster');
var net = require('net');
var events = require('events');
//var process = require('process');
var eventEmitter = new events.EventEmitter();


var amountOfCores = os.cpus().length;
var port = 7000;
var ip = 'localhost';



var connectionProcessAndPorts = new Array([]);
var worker;
var connCount = 0;
if(cluster.isMaster){
	for(var i = 0; i < amountOfCores - 1; i++){
		worker = cluster.fork();
		worker.on('message', function(msg) {
				connCount++;
				var procNum = msg.processNumber.toString();
				//connectionProcessAndPorts[itr][msg.connected] = procNum;
				console.log("Process " + msg.processNumber + " got a connection from: " + msg.connected);
				console.log(connCount);
		});
	}
}
else{	

  	console.log('This is from worker ' + process.pid + ' waiting for new connections, sir.');

  	net.createServer(function(socket){
  		process.send({connected: socket.remotePort, processNumber: process.pid});
	}).listen(port, ip);
}

  
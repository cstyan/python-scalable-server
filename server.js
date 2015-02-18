var os = require('os');
var cluster = require('cluster');
var net = require('net');
var events = require('events');
//var process = require('process');
var eventEmitter = new events.EventEmitter();


var amountOfCores = os.cpus().length;
var port = 7000;
var ip = 'localhost';

var TotalConnectionInfo = function(){
	this.totalDataTransferred = 0;
	this.totalConnectionsMade = 0;

	this.incrementTotalDataTransferred = function(dataAmount){
		this.totalDataTransferred += dataAmount;
	}

	this.incrementTotalConnectionsMade = function(){
		this.totalConnectionsMade++;
	}

	 this.toString = function(){
		console.log("Total amount of connections made: " + this.totalConnectionsMade + "\n Total amount of bytes transferred: " + this.totalDataTransferred);
	}
}


var IndividualConnectionInfo = function(processId, portNumber){
	this.processId = processId;
	this.portNumber = portNumber;
	this.dataSent = 0;

	this.incrementDataSent = function(dataAmount){
		this.dataSent += dataAmount;
	}

	this.toString = function(){
		console.log("The connection on process " + this.processId + " and on portNumber " + 
			this.portNumber + "has sent " + this.dataSent + " bytes of data.")
	}
};


var worker;

if(cluster.isMaster){
	var tci = new TotalConnectionInfo();
var connectionProcessAndPorts = [];

	for(var i = 0; i < amountOfCores - 1; i++){
		worker = cluster.fork();
		worker.on('message', function(msg) {
				if(msg.remotePort != null){
					tci.incrementTotalConnectionsMade();
					connectionProcessAndPorts[msg.processNumber + ":" + msg.remotePort] = new IndividualConnectionInfo(msg.processNumber, msg.remotePort);
					
				}
				else if(msg.connectionId){
				
					connectionProcessAndPorts[msg.connectionId].incrementDataSent(msg.bytesRecievedFromSocket);
					tci.incrementTotalDataTransferred(msg.bytesRecievedFromSocket);
				}

		});

		
	}
	setInterval(function(){

			tci.toString();
		}, 5000);
}
else{	

  	console.log('This is from worker ' + process.pid + ' waiting for new connections, sir.');

  	net.createServer(function(socket){
		
		process.send({remotePort: socket.remotePort, processNumber: process.pid});

  		socket.on('data',function(recievedData){
  			data = recievedData;
  			process.send({connectionId: process.pid + ":" + socket.remotePort ,bytesRecievedFromSocket: recievedData.length});
  			socket.write(recievedData);
  		});

	}).listen(port, ip);
}

  
console.log('Servidor funcionando')

var socket = io.connect('http://' + document.location.hostname + ':' + location.port);

socket.on('mqtt_message', function(data) {
    console.log(JSON.stringify(data));
});
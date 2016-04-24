var ws;
var wsMessageCallbacks = [];

function wsOpen(e) {
    console.log({onopen: arguments});
}

function wsMessage(e) {
    console.log({onmessage: arguments});
    data = JSON.parse(e.data);
    wsMessageCallbacks.forEach(function(cb){cb(data);});
}

function wsClose(e) {
    console.log({onclose: arguments});
}

$(function() {
    ws = new ReconnectingWebSocket(wsUrl);
    ws.onmessage = wsMessage;
    ws.onopen = wsOpen;
    ws.onclose = wsClose;
});

function registerWsMessageCallback(cb) {
    wsMessageCallbacks = wsMessageCallbacks.concat([cb]);
}

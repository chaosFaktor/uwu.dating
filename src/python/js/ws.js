class MessageTemplate {
    static MESSAGE_TYPES = {
        REGISTER_MATCH: "match/register",
        CHAT_CONNECT: "chat/connect"
    }
    type = null;
    constructor() {
    }
}
class MessageBuilder {
    static input = null;
    constructor(input) {
        if (input) {
            this.input = input;
        } else {
            this.input = new MessageTemplate()
        }
    }
    set_type(type) {
        this.input.type = type;
        return this
    }
    get_result() {
        return this.input;
    }
}
class WebSocketCom {
    constructor(on_open=null, on_msg=null) {
        this.load_socket()
        if (on_open != null) {
            this.socket.addEventListener("message", on_open);
        }
        if (on_msg != null) {
            this.socket.addEventListener("open", on_msg);
        }
        

    }
    load_socket() {
        let loc = window.location, new_uri;
        if (loc.protocol === "https:") {
            new_uri = "wss:";
        } else {
            new_uri = "ws:";
        }
        new_uri += "//" + loc.hostname + ":" + loc.port;
        new_uri += "/ws";
        this.socket = new WebSocket(new_uri);
        this.socket.onerror = event=>{
            this.load_socket();
        }
    }
    register_on_open(callback) {
        if (this.socket.readyState == WebSocket.OPEN) {
            callback();
        } else {
            this.socket.addEventListener("open", callback);
        }
    }
    register_on_message(callback) {
        if (this.socket.readyState == WebSocket.OPEN) {
            callback();
        } else {
            this.socket.addEventListener("message", callback)
        }
    }
    get_state() {
        return this.socket.readyState;
    }
    async await_open() {
        return new Promise((resolve, reject)=>{
            this.register_on_open(resolve);
        });
    }
    send(data) {
        if (this.socket.readyState == WebSocket.OPEN) {
            this.socket.send(data)
        }
    }
}

App.WebSocketCom = WebSocketCom;
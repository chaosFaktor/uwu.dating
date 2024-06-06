class ViewChatMessage {
    static Type = {
        NARRATION: 0,
        OWN: 1,
        NOT_OWN: 2        
    }
}
class ViewChatMessageBuilder {
    msg = null;
    text_box = null;
    constructor(msg, text_box) {
        if (msg != null) {
            this.msg = msg;            
        } else {
            this.msg = document.createElement("div");
        }
        if (text_box != null) {
            this.text_box = text_box;
        } else {
            this.text_box = $(".text_box_container").get();
        }
    }
    set_text(text) {
        this.msg.innerText = text;
        return this
    }
    set_type(type) {
        if (type == ViewChatMessage.Type.NARRATION) {
            this.msg.classList = ["narration_msg"];
        } else if (type == ViewChatMessage.Type.OWN) {
            this.msg.classList.add("user_msg");
            this.msg.classList.add("own_msg");
        } else if (type == ViewChatMessage.Type.NOT_OWN) {
            this.msg.classList.add("user_msg");
            this.msg.classList.add("not_own_msg");
        }
        return this;
    }
    display() {
        this.text_box.appendChild(this.msg);
        this.text_box.scrollTop = this.text_box.scrollHeight;
        return this.text_box
    }
}

con = new App.WebSocketCom();

function send_msg() {
    let text = $("#message_input").val();
    if (text.trim() == "") {
        return
    }
    $("#message_input").val("");
    
    con.await_open().then(event=>{
        con.send(JSON.stringify({
            "type": "chat/message",
            "text": text
        }));
    })

    new ViewChatMessageBuilder()
        .set_text(text)
        .set_type(ViewChatMessage.Type.OWN)
        .display();
    
        
}
$(document).ready(event=>{
    $("#send_btn").on("click", event=>{
        send_msg();
    });
    $("#message_input").get().addEventListener("keypress", function(event) {
        if (event.key == "Enter") {
            send_msg();
        }
    })


    con.register_on_message(event=>{
        let msg = JSON.parse(event.data);
        if (msg.type == "chat/connect") {
            if (!msg.success) {
                setTimeout(event=>{
                    con.send(JSON.stringify({
                        type: "chat/connect"
                    }))
                }, 800);
            } else {
                new ViewChatMessageBuilder()
                    .set_type(ViewChatMessage.Type.NARRATION)
                    .set_text("The other participant connected to chat.")
                    .display();
            }
        } else if (msg.type= "chat/message") {
            if (!msg.text) {
                return;
            }
            console.log(msg);
            new ViewChatMessageBuilder()
                .set_type(ViewChatMessage.Type.NOT_OWN)
                .set_text(msg.text)
                .display();
        } else if (msg.type= "chat/disconnect") {
            new ViewChatMessage()
                .set_type(ViewChatMessage.Type.NARRATION)
                .set_text("The other participant closed the chat, but may reconnect.")
                .display();
        } else {
        }
    });
    con.await_open().then(event=>{
        con.send(JSON.stringify({
            type: "chat/connect"
        }));
        
    })
})
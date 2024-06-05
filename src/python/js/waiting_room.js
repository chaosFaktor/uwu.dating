let send_match_interval = null;
class View {
    static start_time = Date.now();
    static display_waiting_since_text_interval = null;
    static display_waiting_since_text(text) {
        $("#waiting_since").html(text);
    }
    static timer = setInterval(event=>{
        let uptime = Math.floor((Date.now() - this.start_time) /1000);
        View.display_waiting_since_text(uptime);
    }, 1000);

}


con = new App.WebSocketCom();
con.register_on_message(event=>{
    let msg = JSON.parse(event.data);
    if (msg.type == "match/found") {
        send_match_interval = null;
        window.location.href="/app/chat"
    } else if (msg.type == "match/notfound" && send_match_interval != null) {
        alert("hi")
        con.send(JSON.stringify(
            new MessageBuilder()
            .set_type(MessageTemplate.MESSAGE_TYPES.REGISTER_MATCH)
            .get_result()
        )
        )
    }
})
con.await_open().then(event=>{
    send_match_interval = setInterval(event=>{
        con.send(JSON.stringify(
            new MessageBuilder()
            .set_type(MessageTemplate.MESSAGE_TYPES.REGISTER_MATCH)
            .get_result()
        ));
    }, 1000)
})
App.View = View;
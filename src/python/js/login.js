let values = {};
$("form").each(element=>{
    element.on("submit", event=>{
        const data = new FormData(element.get());
        for (const [name,value] of data) {
            values[name] = value;
        }

        App.Section.slide_to_next_section();

    });
    
});
async function login(event) {
    await fetch("/login_do", {
      method: "POST",
      headers: {'Content-Type': 'application/json'}, 
      body: JSON.stringify(values)
    });
}
$("#submit-form").on("submit", event=>{
    login().then(event=>{
        setTimeout(event=>{
            window.location.href = "/app/waiting_room";
        }, 1000);
    });
})
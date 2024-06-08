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
async function login(action = "/login_do", method = "post") {
    
    let form_obj = document.createElement("form");
    $(form_obj).attr("method", method);
    $(form_obj).attr("action", action);
    
    console.log(values);
    console.log(Object.entries(values));
    let input;
    for (let [key, value] of Object.entries(values)) {
        input = document.createElement("input");
        $(input).attr("name", key);
        $(input).val(value);
        $(form_obj).append(input);

    }
    $("body").append(form_obj);
    form_obj.submit();
    return;

}
$("#submit-form").on("submit", event=>{
    login().then(event=>{
        setTimeout(event=>{
        }, 1000);
    });
})
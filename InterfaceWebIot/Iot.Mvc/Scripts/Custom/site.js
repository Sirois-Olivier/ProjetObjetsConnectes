
function SendMessage() {

    alert();

    $.ajax({
        type: "POST",
        url: '/Home/SendMessage',
        data: param = "",
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    })
}
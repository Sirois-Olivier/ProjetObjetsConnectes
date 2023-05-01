
function SendMessage() {

    $.ajax({
        type: "POST",
        url: '/Home/SendMessage',
        data: { },
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    })
}
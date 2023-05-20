
function SendMessageOpenDoor() {

    $.ajax({
        type: "POST",
        url: '/Home/SendMessageOpenDoor',
        data: { },
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: "json"
    })
}

function SendMessageCloseDoor() {
    $.ajax({
        type: "POST",
        url: '/Home/SendMessageCloseDoor',
        data: {},
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: "json"
    })
}

function SendMessageSetAutomatic() {
    $.ajax({
        type: "POST",
        url: '/Home/SendMessageSetAutomatic',
        data: {},
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: "json"
    })
}


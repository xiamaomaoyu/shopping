
var users = [];
var current = "";
var image_base64 = "";
var input = $("#user_input");


var socket = io.connect('http://127.0.0.1' + ':' + '5000');

socket.on('staff', function( msg ) {
    var user_id = msg.user_id;
    var info = unescape(msg.user_message);
    var img_64 = unescape(msg.user_image);
    // make notify
    // notifyMe(info);

    var onclick_id = "\'"+user_id+ "\'";
    var dt = new Date();
    var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();

    // if not exists we need create the user chat page
    if (jQuery.inArray(user_id, users) === -1) {
        users.push(user_id);
        var people = $("<ul class=\"people\" id=\"" + user_id + "u" + "\"" + "onClick=\"set_activity("  + onclick_id + ")\">" +
                "<li class=\"person\" id=\"" + user_id + "p" + "\">" +
                "<img src=\"../static/dog.png\" alt=\"\" />" +
                "<span class=\"name\">" + user_id + "</span>" +
                "<span class=\"time\" id=\"" + user_id + "t" + "\">" + time + "</span>" +
                "<span class=\"preview\" style=\"color: red\" id=\"" + user_id + "s" + "\">" + info + "</span>" +
                "</li>" +
                "</ul>");


        var chat_content = "<div style=\"display: none\" id=\"" + user_id + "ch" + "\">" +
                "<div class=\"top\"><span>To: <span class=\"name\">" + user_id + "</span></span></div>" +
                "<div class=\"chat\" style=\"height: 80%; overflow: auto\" id=\"" + user_id + "c" + "\">" +
                "<div class=\"conversation-start\">" + time + "</div>";

        if (info !== "") {
            chat_content += "<div class=\"bubble you\">" + info + "</div>";
        }

        if (img_64 !== "") {
            if (img_64.indexOf("video") >= 0) {
                 chat_content += "<div class=\"bubble you\">" +
                    "<video width=\"350px\" height=\"320px\" " +
                    "x-webkit-airplay=\"true\" webkit-playsinline=\"true\"" +
                    " onclick=\"view_play(this)\"" +
                    " src=\"" + img_64 + "\">" + "</video></div>";
            } else {
                chat_content += "<div class=\"bubble you\">" +
                    "<img width=\"350px\" " +
                    "height=\"320px\" src=\"" + img_64 + "\">" +
                    "</div>";
            }
        }

        chat_content += "</div>" +
                        "</div>";

        /**
        var people_chat = $("<div style=\"display: none\" id=\"" + user_id + "ch" + "\">" +
                "<div class=\"top\"><span>To: <span class=\"name\">" + user_id + "</span></span></div>" +
                "<div class=\"chat\" style=\"height: 80%; overflow: auto\" id=\"" + user_id + "c" + "\">" +
                "<div class=\"conversation-start\">" + time + "</div>" +
                "<div class=\"bubble you\">" + info +
                "</div>" +
                "</div>" +
                "</div>");
         **/

        $("#chat_peoples").prepend(people);
        $("#chat_info").append(chat_content);

    } else {
        var chat = $("#chat_peoples");
        var user = "#" + user_id + "u";
        var user_span = "#" + user_id + "s";
        var user_time = "#" + user_id + "t";
        var user_chat = "#" + user_id + "c";

        $(user).remove();
        chat.prepend($("<ul class=\"people\" id=\"" + user_id + "u" + "\"" + "onclick=\"set_activity(" + "\'"+ user_id + "\'"+ ")\">" +
                "<li class=\"person\" id=\"" + user_id + "p" + "\">" +
                "<img src=\"../static/dog.png\" alt=\"\" />" +
                "<span class=\"name\">" + user_id + "</span>" +
                "<span class=\"time\" id=\"" + user_id + "t" + "\">" + time + "</span>" +
                "<span class=\"preview\" style=\"color: red\" id=\"" + user_id + "s" + "\">" + info + "</span>" +
                "</li>" +
                "</ul>"));

        $(user_span).val(info);
        $(user_span).css('color', 'red');
        $(user_time).val(time);

        if (info !== "") {
            $(user_chat).append("<div class=\"bubble you\">" + info + "</div>");
        }

        if (img_64 !== "") {
            if (img_64.indexOf("video") >= 0) {
                $(user_chat).append("<div class=\"bubble you\">" +
                    "<video width=\"350px\" height=\"320px\" " +
                    "x-webkit-airplay=\"true\" webkit-playsinline=\"true\"" +
                    " onclick=\"view_play(this)\"" +
                    " src=\"" + img_64 + "\">" + "</video></div>");
            } else {
                $(user_chat).append("<div class=\"bubble you\">" +
                    "<img width=\"350px\" " +
                    "height=\"320px\" src=\"" + img_64 + "\">" +
                    "</div>");
            }
        }

        var current_user = "#" + current + "p";
        $(current_user).removeClass("active");
        $(current_user).addClass("active");

        if (current !== "") {
            var current_input = "#" + current + "c";
            $(current_input).scrollTop($(current_input)[0].scrollHeight);
        }
    }

});



function set_activity(user_id) {

    var active_people = "#" + user_id + "p";
    var people_chat = "#" + user_id + "ch";
    var chat_span = "#" + user_id + "s";

    if (current !== "") {
        var current_user = "#" + current + "p";
        var current_chat = "#" + current + "ch";
        $(current_user).removeClass("active");
        $(current_chat).hide();
        current = user_id;
    } else {
        current = user_id;
    }

    $(active_people).addClass("active");
    $(people_chat).show();
    $(chat_span).css("color", "gary");

    var current_input = "#" + current + "c";
    $(current_input).scrollTop($(current_input)[0].scrollHeight);
}


window.onkeydown = function(event){
    if(event.keyCode === 13){
        if((input.val() !== "" || image_base64 !== "") && current !== ""){
            send_msg(input.val());
        }
    }
};

$("#send_btn").click(function () {
    if ((input.val() !== "" || image_base64 !== "") && current !== "") {
        send_msg(input.val());
    }
    console.log('here');
});

function send_msg(message) {
    var user_chat = "#" + current + "c";

    socket.emit('staff post', {
       user_message: escape(message),
       user_image: escape(image_base64),
       user_id: current
    });

    if (message !== "") {
        $(user_chat).append("<div class=\"bubble me\">" + message + "</div>");
    }

    if (image_base64 !== "") {
        if (image_base64.indexOf("video") >= 0) {
            $(user_chat).append("<div class=\"bubble me\">" +
                "<video width=\"350px;\" x-webkit-airplay=\"true\" " +
                "webkit-playsinline=\"true\" height=\"320px;\" " +
                "onclick=\"view_play(this)\" src=\"" + image_base64 + "\">" +
                "</video></div>");
        } else {
            $(user_chat).append("<div class=\"bubble me\">" +
                "<img width=\"350px;\" height=\"320px;\" " +
                "src=\"" + image_base64 + "\">" + "</div>");
        }
    }

    input.val('').focus();
    update(message);
}


function update(info) {
    var current_input = "#" + current + "c";
    var active_people = "#" + current + "p";

    $(current_input).scrollTop($(current_input)[0].scrollHeight);


    var dt = new Date();
    var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
    var chat = $("#chat_peoples");
    var user = "#" + current + "u";

    $(user).remove();
    chat.prepend($("<ul class=\"people\" id=\"" + current + "u" + "\"" + "onclick=\"set_activity(" + "\'" +  current + "\'" +")\">" +
            "<li class=\"person\" id=\"" + current + "p" + "\">" +
            "<img src=\"../static/dog.png\" alt=\"\" />" +
            "<span class=\"name\">" + current + "</span>" +
            "<span class=\"time\" id=\"" + current + "t" + "\">" + time + "</span>" +
            "<span class=\"preview\" style=\"color: gray\" id=\"" + current + "s" + "\">" + info + "</span>" +
            "</li>" +
            "</ul>"));

    var current_user = "#" + current + "p";
    $(current_user).removeClass("active");

    $(active_people).addClass("active");

    image_base64 = "";
}

try {
    socket.on('leave', function (str) {
        var user = "#" + str + "u";
        var user_chat = "#" + str + "ch";
        $(user).remove();
        $(user_chat).remove();
        current = "";
    });
} catch (e) {
    socket.close();
}


// set onclick of attachment
$("#attach").click(function () {
    $("#img").click();
});

// generate the base64 for image
function encodeImageToBase64(element) {
    var acceptedImageTypes = ['image/gif', 'image/jpeg', 'image/png','video/mp4'];

    var file = element.files[0];
    var reader = new FileReader();

    if (acceptedImageTypes.indexOf(file.type) === -1) {
        image_base64 = "";
        return;
    }

    reader.onloadend = function() {
        image_base64 = reader.result;
    };
    reader.readAsDataURL(file);

}

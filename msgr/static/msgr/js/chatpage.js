
$(window).on('visibilitychange', function(event) {
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    navigator.sendBeacon(full_path, data);
});


var page = 1;

function load_messages() {
    $.ajax({
        url: messages_path,
        type: 'GET',
        data: {page: page},

        success: function(json) {
            $('#messages-list').append(json.messages_rendered);
            if (page == 1) {
                latest_pk = json.first_item_pk;
                get_updates();
            }
        },
    });
}

load_messages();

$(window).scroll(function() {
    if ($(window).scrollTop() >= ($(document).height() - $(window).outerHeight(true) - 1)) {
        page += 1;
        load_messages();
    }
});

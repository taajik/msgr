
var latest_pk = 0;
function get_messages() {
    $.ajax({
        url: full_path,
        type: 'GET',
        data: {update: true, latest_pk: latest_pk},

        success: function(json) {
            if (json.latest_pk) {
                $('#messages-list').prepend(json.message_items);
                latest_pk = json.latest_pk;
            }
        },

        complete: function(data) {
            setTimeout(get_messages, 1000);
        }
    });
}

get_messages();


$('#message-form').on('submit', function(event) {
    event.preventDefault();
    send_message(this);
    $(window).scrollTop(0);
});

function send_message(form) {
    $.ajax({
        url: full_path,
        type: 'POST',
        data: $(form).serialize(),

        success: function() {
            $('#message-field').val('');
        },

        error: function(data) {
            console.log('Error: ' + data.responseText);
        }
    });
}

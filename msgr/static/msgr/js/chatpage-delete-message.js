
var modal = $('#delete-confirm');

function open_modal(message) {
    $('#delete-pk').val(message);
    $('#m-'+message).css('background-color', '#618d3d');
    modal.css('display', 'block');
}

function close_modal() {
    $('#m-'+$('#delete-pk').val()).css('background-color', '');
    modal.css('display', 'none');
}

$(window).click(function(event) {
    if ($(event.target).is(modal)) {
        close_modal();
    }
});


$('#delete-form').submit(function(event) {
    event.preventDefault();
    var data = new FormData(this);
    navigator.sendBeacon(delete_message_path, data);
    $('#m-'+data.get('message')).remove();
});

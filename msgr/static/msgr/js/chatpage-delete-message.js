
var modal = document.getElementById('delete-confirm');

function open_modal(message) {
    $('#delete-pk').val(message);
    modal.style.display = 'block';
}

function close_modal() {
    modal.style.display = 'none';
}

$(window).click(function(event) {
    if (event.target == modal) {
        close_modal();
    }
});


$('#delete-form').submit(function(event) {
    event.preventDefault();
    var data = new FormData(this);
    navigator.sendBeacon(delete_message_path, data);
    $('#m-'+data.get('message')).remove();
});

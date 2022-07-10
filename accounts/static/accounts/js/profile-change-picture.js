
function preview(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#the-picture').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$('#id_picture').change(function() {
    preview(this);
});


var date_headers = [];

function add_date_headers(messages) {
    var date;
    $($('.m-date', $(messages)).get().reverse()).each(function(i, obj) {
        date = $(obj).text();
        if (!date_headers.includes(date)) {
            date_headers.push(date);
            $('<br style="clear: both;"><div class="date-header">'+date+'</div>').insertAfter(
                $('#'+$(obj).parent().attr("id"))
            );
        }
    });
}

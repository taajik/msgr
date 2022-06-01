
var menu = $("#menu-wrapper");
var header = $('#header');

function open_menu() {
    menu.css('height', '100%');
}

$(window).click(function(event) {
    if (header.has(event.target).length == 0) {
        menu.css('height', '0');
    }
});

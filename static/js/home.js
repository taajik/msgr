
var blank = $('.blank');

function remove_blank(i) {
    $(blank[i]).css('height', '0');
    i += 1;
    if (i < blank.length) {
        setTimeout(remove_blank, 1500, i);
    }
};

remove_blank(0);

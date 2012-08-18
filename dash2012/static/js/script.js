function center (element, outer) {
    element.css("left", ( outer.width() - element.outerWidth() ) / 2+outer.scrollLeft() + "px");
    return element;
};

function centerHeight (element, outer) {
    element.css("top", ( outer.height() - element.outerHeight() ) / 2+outer.scrollTop() + "px");
    return element;
};

$(document).ready(function() {
    $('.actions-trigger').click(function() {
        $(this).toggleClass('open');
        $(this).next('.actions-dropdown').toggle('fast');
    });

});
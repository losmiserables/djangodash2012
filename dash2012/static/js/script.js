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
        $('.actions-trigger').removeClass('open');
        $('.actions-dropdown').hide();
        $(this).toggleClass('open');
        $(this).next('.actions-dropdown').toggle('fast');
    });

    $(document).click(function(){
        $('.actions-dropdown').hide();
        $('.actions-trigger').removeClass('open');

    });

    $(".actions-trigger").click(function(e){
        e.stopPropagation();
    });

    $('.select-trigger').click(function() {
        $(this).toggleClass('open');
        $(this).next('.select-dropdown').toggle('fast');
    });

    $(document).click(function(){
        $('.select-dropdown').hide();
        $('.select-trigger').removeClass('open');

    });

    $(".select-holder").click(function(e){
        e.stopPropagation();
    });

});
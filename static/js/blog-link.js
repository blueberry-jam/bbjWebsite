$(document).ready(function() {
    $('.post-container').click(function() { 
        var dclass = $('.post-container').attr('id');
        window.location.href = `blog/${event.target.id}`;
    });
});
$(document).ready(function() {
    $("#post-button").click(function(){
        var title = $.trim($('#blog-title-input').val());
        var desc = $.trim($('#blog-desc-textarea').val());
        var body = $.trim($('#blog-body-textarea').val());
        var sub = true;
        if(title != '') {
            $('#id_title').val(title);
            if($('#e1').css('display') === 'block') {
                $('#e1').css('display', 'none');
                var sub = true;
            }
        }
        else {
            $('#e1').css('display', 'block');
            var sub = false;
        }
        if(desc != '') {
            $('#id_description').val(desc);
            if($('#e2').css('display') === 'block') {
                $('#e2').css('display', 'none');
                var sub = true;
            }
        }
        else {
            $('#e2').css('display', 'block');
            var sub = false;
        }
        if(body != '') {
            $('#id_body').val(body);
            if($('#e3').css('display') === 'block') {
                $('#e3').css('display', 'none');
                var sub = true;
            }
        }
        else {
            $('#e3').css('display', 'block');
            var sub = false;
        }
        if(sub == true) {
            $('#post-button-submit').click();
        }
    });
});
$(document).ready(function() {
    $('#delete-button').click(function() {
        $('#id_delete').val('yes')
        $('#post-button-submit').click()
    });
});
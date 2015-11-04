$('.document').ready(function(){
    getCaptcha(function(data){
        var str = 'F(' + data + ')';
        $('#captcha').html(str);
    });
});

var getCaptcha = function(succes){
    $.ajax({
        url:'/x/',
        success: succes
    });
};

$(function(){
  $('#loginForm').submit(function(){
    $.post($(this).attr('action'), $(this).serialize(), function(json) {
        if (json !== true) {
            alert('wrong data');
            $('#loginForm').find('input[type=text], input[type=password], textarea').val('');
        } else {
            window.location.href = 'view/';
        }
    }, 'json');
    return false;
  });
});

var checkCaptcha = function(captcha){
    return $.ajax({
        url:'/check-captcha/',
        data: {y:captcha},
        method: 'post'
    });
};
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
            window.location.href = 'read/';
            setInterval(function () {
                getCaptcha(function (captcha) {
                    var captchaText = 'please enter captcha: F(' + captcha + ') = ?';
                    var result = prompt(captchaText);
                    var res = checkCaptcha(result);
                    if (res !== true) {
                        window.location.href = '/'
                    }
                })
            }, 5000);
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
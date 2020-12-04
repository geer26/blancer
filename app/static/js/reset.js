socket = io();


var pw_ok = false;
var pwd = '';
var pwd_strength = 0;

var reg_strlo = /[abcdefghijklmnopqrstuvwxyz]+/;
var reg_strhi = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]+/;
var reg_num = /[0-9]+/;
var reg_strspec = /[!@#$%^&*?_~]+/;


function send_message(e_name,message){
    socket.emit(e_name,message);
};


socket.on('newmessage', function(data){
    switch (data['event']){

        //here is an error message, show it to user! - DONE
        case 191:{
            $('#pagecontent').append(data['htm']);
                $('#error_modal').click(function(){
                    $('#error_modal').remove();
                })
            }
            break;

        case 1272:{
            location.href=data['location'].toString();
            }
            break;

    }
});


function req_for_error(message){
    var data = {event: 291, message:message};
    send_message('newmessage', data);
};


function resetpw(){

    if (!$('#reset_username').val()||!$('#reset_code').val()||!$('#reset_password').val()||!$('#reset_password2').val()){
        req_for_error('All fields must be filled!');
        $('#reset_password').val('');
        $('#reset_password2').val('');
        $('#reset_code').val('');
        return;
    }

    if($('#reset_password').val() != $('#reset_password2').val()){
        req_for_error('The passwords do not match!');
        $('#reset_password').val('');
        $('#reset_password2').val('');
        $('#reset_code').val('');
        return;
    }

    if (pw_ok){
        var token = $('#token').val();
        var username = $('#reset_username').val();
        var val_code = $('#reset_code').val();
        var pw1 = $('#reset_password').val();
        var pw2 = $('#reset_password2').val();
        var data = {event: 2272, token: token, uname: username, code: val_code, p1: pw1, p2: pw2};
        send_message('newmessage', data);
        return;
    }

    else{
        req_for_error('The password is too weak!');
        $('#reset_password').val('');
        $('#reset_password2').val('');
        $('#reset_code').val('');
        return;
    }

};


function checkpwd(){

    pwd = $('#reset_password').val();

    document.getElementById('pwdstatus').classList.remove("none");
    document.getElementById('pwdstatus').classList.remove("weak");
    document.getElementById('pwdstatus').classList.remove("better");
    document.getElementById('pwdstatus').classList.remove("strong");

    pwd_strength = 0;

    if (pwd.length >= 8){pwd_strength += 32;}

    if ( pwd.length >= 8 && reg_strlo.test(pwd) ){pwd_strength += 6;}

    if ( pwd.length >= 8 && reg_strhi.test(pwd) ){pwd_strength += 6;}

    if ( pwd.length >= 8 && reg_num.test(pwd) ){pwd_strength += 6;}

    if ( pwd.length >= 8 && reg_strlo.test(pwd) && reg_strhi.test(pwd) && reg_num.test(pwd) ){pwd_strength += 1;}

    if ( pwd.length >= 8 && reg_strlo.test(pwd) && reg_strhi.test(pwd) && reg_num.test(pwd) &&reg_strspec.test(pwd) ){pwd_strength += 25;}

    if (pwd_strength > 100){pwd_strength=99;}

    if(25 >= pwd_strength && pwd_strength >= 0){
    document.getElementById('pwdstatus').classList.add("none");
    document.getElementById('pwdstatus').innerText ="Very weak!";

    var pw_ok = false;
    }

    if(50 >= pwd_strength && pwd_strength >= 26){
    document.getElementById('pwdstatus').classList.add("weak");
    document.getElementById('pwdstatus').innerText ="Weak!";

    var pw_ok = false;
    }

    if(75 >= pwd_strength && pwd_strength >= 51){
    $('#pwdstatus').addClass('better');
    document.getElementById('pwdstatus').innerText ="Strong enough!";

    var pw_ok = true;
    }

    if(100 >= pwd_strength && pwd_strength >= 76){
    $('#pwdstatus').addClass('strong');
    document.getElementById('pwdstatus').innerText ="Very strong!";

    var pw_ok = true;
    }

};
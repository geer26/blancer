socket = io();


var pw_ok = false;
var pwd = '';
var pwd_strength = 0;

var m_strUpperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
var m_strLowerCase = "abcdefghijklmnopqrstuvwxyz";
var m_strNumber = "0123456789";
var m_strCharacters = "!@#$%^&*?_~"

var reg_strlo = /[a-z]+/i;
var reg_strhi = /[A-Z]+/i;
var reg_num = /[0-9]+/;
var reg_strspec = /[!@#$%^&*?_~]+/i;


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

    //TODO check password complexity

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

    pwd_strength = 1;

    if (pwd.length >= 8){pwd_strength += 32;}



    if (pwd_strength > 100){pwd_strength=99;}

    console.log(pwd_strength);

    if(25 >= pwd_strength && pwd_strength >= 0){
    console.log('very weak');
    //very weak
    //remove all class
    //$('#pwdstatus').removeClass();
    //add weak class
    document.getElementById('pwdstatus').classList.add("none");
    //add inner text"
    document.getElementById('pwdstatus').innerText ="Very weak!";

    var pw_ok = false;
    }

    if(50 >= pwd_strength && pwd_strength >= 26){
    console.log('weak');
    //weak
    //remove all class
    //$('#pwdstatus').removeClass();
    //add weak class
    document.getElementById('pwdstatus').classList.add("weak");
    //add inner text"
    document.getElementById('pwdstatus').innerText ="Weak!";

    var pw_ok = false;
    }

    if(75 >= pwd_strength && pwd_strength >= 51){
    console.log('better');
    //better
    //remove all class
    //$('#pwdstatus').removeClass();
    //add weak class
    $('#pwdstatus').addClass('better');
    //add inner text"
    document.getElementById('pwdstatus').innerText ="Strong enough!";

    var pw_ok = true;
    }

    if(100 >= pwd_strength && pwd_strength >= 76){
    console.log('strong');
    //strong
    //remove all class
    //$('#pwdstatus').removeClass();
    //add weak class
    $('#pwdstatus').addClass('strong');
    //add inner text"
    document.getElementById('pwdstatus').innerText ="Very strong!";

    var pw_ok = true;
    }

};
socket = io();

function send_message(e_name,message){
    socket.emit(e_name,message);
};

socket.on('newmessage', function(data){
    switch (data['event']){

        //here is an error message, show it to user! - DONE
        case 191:{
            $('#pagecontent').append(data['htm']);
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
    var token = $('#token').val();
    var username = $('##reset_username').val('');
    var val_code = $('#reset_code').val('');
    var pw1 = $('#reset_password').val('');
    var pw2 = $('#reset_password2').val('');
    var data = {event: 2272, token: token, username: username, val_code: val_code, pw1: pw1, pw2: pw2};
    send_message('newmessage', data);
};
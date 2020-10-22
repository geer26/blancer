
socket = io();

function send_message(e_name,message){
    socket.emit(e_name,message);
};


$('.modal').modal({

});


$('#signupbutton').click(function(){
    if ( $('#signup_username').val() && $('#signup_email').val() && $('#signup_password').val() && $('#signup_password2').val() && $('#signup_agree').prop('checked') ){
        var data = {
        event: 211,
        username: $('#signup_username').val(),
        email: $('#signup_email').val(),
        password1: $('#signup_password').val(),
        password2: $('#signup_password2').val(),
        agreed: $('#signup_agree').prop('checked')
        };
        send_message('newmessage', data);
    } else{
        var data ={event: 291, message:'Fill all the inputs!'};
        send_message('newmessage', data);
    }
});


$('#loginbutton').click(function(){
    if ( $('#login_username').val() && $('#login_password').val() ){
        var data = {
        event: 221,
        username: $('#login_username').val(),
        password: $('#login_password').val(),
        remember: $('#input_remember').prop('checked')
        };
        send_message('newmessage', data);
    } else{
        var data ={event: 291, message:'Fill all the inputs!'};
        send_message('newmessage', data);
    };
});


//event dispatcher
socket.on('newmessage', function(data){
    switch (data['event']){
        //signed up, user created! - READY
        case 111:
            {
            $('#signup_username').val('');
            $('#signup_email').val('');
            $('#signup_password').val('');
            $('#signup_password2').val('');
            $('#signup_agree').prop("checked", false);
            $('#signupmodal').modal('close');
            $('#pagecontent').append(data['htm']);
            $('#info_modal').click(function(){
                $('#info_modal').remove();
            });
            }
            break;

        //login validated, send loginform!
        case 121:
            if (data['status']){
                var data = {username:$('#login_username').val(), password:$('#login_password').val(), remember_me:$('#input_remember').prop('checked')}
                $.post( '/' , data )
                window.location.reload();
            }
            break;

        //user logged in, refresh page!
        case 122:
            //refresh pagecontent
            window.location.reload();
            console.log('logged in!');
            break;

        //here is an error message, show it to user! - READY
        case 191:
            {
            $('#pagecontent').append(data['htm']);
            $('#error_modal').click(function(){
                $('#error_modal').remove();
            });
            }
            break;
    }
});



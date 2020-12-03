socket = io();

function send_message(e_name,message){
    socket.emit(e_name,message);
};

socket.on('newmessage', function(data){
    switch (data['event']){

        //password reseted ok, redirect to mainpage!
        case 111:{
            $('#signup_username').val('');
            $('#signup_email').val('');
            $('#signup_password').val('');
            $('#signup_password2').val('');
            $('#signup_agree').prop("checked", false);

            hideitem('signup_frame', 'signupmodal')

            $('#pagecontent').append(data['htm']);
            animateCSS('#info_frame', inanim);
            }
            break;

        //TODO - implement something!

    }
});

function resetpw(){
    console.log('RESET PASSWORD!');
};
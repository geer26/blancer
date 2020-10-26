
socket = io();

function send_message(e_name,message){
    socket.emit(e_name,message);
};


$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton({
    });

    $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
    });

    $('.modal').modal({
    });

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

        //here is an error message, show it to user! - READY
        case 191:
            {
            $('#pagecontent').append(data['htm']);
            $('#error_modal').click(function(){
                $('#error_modal').remove();
            });
            }
            break;

        //here is an addpocket modal, use it wisely!
        case 141:
            {
            $('#pagecontent').append(data['htm']);
            $('#close_modal').click(function(){
                $('#addpocket_modal').remove();
                });
            $('#add_pocket').click(function(){
                //include check!
                if ($('#addp_bal').val()!='' && isNaN($('#addp_bal').val())){
                    var data ={event: 291, message:'Initial balance must be a nuber or leave it blank!'};
                    send_message('newmessage', data);
                    $('#addp_bal').val('');
                }

                else if (!$('#addp_name').val()){
                    var data ={event: 291, message:'A name must be set for this pocket!'};
                    send_message('newmessage', data);
                }

                else {
                    var data ={ event: 243, p_name: $('#addp_name').val(), p_desc: $('#addp_desc').val(), p_balance: $('#addp_bal').val() };
                    send_message('newmessage', data);
                }
                });
            }
            break;


        //pocket created successfully, close modal!
        case 148:{
            $('#addpocket_modal').remove();
            $('#usercarousel').remove();
            $('#uc').append(data['htm']);
            location.reload();
            }
            break;


        //del this id row from page
        case 171:
            {
                $('#'+data['to_del']).remove();
            }
            break;
    }
});


function deluser(e){
        var data = {userid: e.id, event: 271};
        send_message('newmessage', data);
};


function addpocket(){
    var data ={event: 241};
    send_message('newmessage', data);
};
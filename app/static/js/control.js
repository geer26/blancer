
socket = io();

var current_slide = 0;
var slide_id = 0;

var inanim = 'fadeIn';
var outanim = 'fadeOut';
var removeanim = 'fadeOutLeft';
var attentionanim = 'rubberBand';

var slides_in_carousel = {};

function send_message(e_name,message){
    socket.emit(e_name,message);
};


$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton({

    });


    $('.tooltipped').tooltip({delay: 50});


    $('input#signup_username, input#signup_email').characterCounter({});


    var car = $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    //indicators: true,
    //noWrap: true,
    onCycleTo: function(data) {
      current_slide = data.id;
      //when user changes page, current slide id will be stored in current_slide as "uc_XXX", where XXX is the id of the pocket
      //console.log(current_slide);
    }
    });


    $('.modal').modal({});

    animateCSS('#logo', inanim);

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

        //signed up, user created!
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

        //login seems to be ok, send the form!
        case 121:{
                submitform('loginform');
            }
            break;

        //here is an error message, show it to user! - DONE
        case 191:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#error_message', inanim);
            }
            break;

        //here is an usercarousel as whole - DONE!
        case 181:{

            $('#usercarousel').remove();

            var cs = data['slides'][current_slide];

            $('#uc').append(data['htm']);
            var car = $('.carousel.carousel-slider').carousel({
                fullWidth: true,
                //indicators: true,
                onCycleTo: function(data) {
                    current_slide = data.id;
                    //when user changes page, current slide id will be stored in current_slide as "uc_XXX", where XXX is the id of the pocket
                    //console.log(current_slide);
                    }
                });
            $('.carousel').carousel('set', cs);
            }
            break;


        //password reset OK
        case 187:{
            console.log('PW RESET OK');
            removeitem('rp_frame', 'rp_modal');
            $('#pagecontent').append(data['htm']);
            animateCSS('#info_frame', inanim);
            }
            break;


        //here is the resetpassword modal
        case 188:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#rp_frame', inanim);
            }
            break;


        //here is the helpmodal, show it to the user!
        case 189:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#help_frame', inanim);
            }
            break;


        //here is an addpocket modal, use it wisely! - DONE
        case 141:{

            $('#pagecontent').append(data['htm']);
            animateCSS('#addm_frame', inanim);
            $('#add_pocket').click(function(){
                //include check!
                if ($('#addp_bal').val()!='' && isNaN($('#addp_bal').val())){
                    var data ={event: 291, message:'Initial balance must be a number or leave it blank!'};
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

            };
            break;


       //user must confirm deletion of pocket - DONE
       case 142:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#delp_confirm', inanim);
            $('#cancelbutton').click(function(){
                /*animateCSS('#delp_confirm', 'bounceOut').then((message) => {
                $('#delpocket_confirm').remove();
                });*/
                removeitem('delp_confirm', 'delpocket_confirm');
            });
            $('#delbutton').click(function(){
                var data = {
                    event: 244,
                    p_id: $('#p_id').text()
                };
                send_message('newmessage', data);
                /*animateCSS('#delp_confirm', outanim).then((message) => {
                $('#delpocket_confirm').remove();
                });*/
                removeitem('delp_confirm', 'delpocket_confirm');
            });
            }
            break;


        //pocket created successfully, close modal! - DONE!
        case 148:{
            removeitem('addm_frame', 'addpocket_modal');
            refresh_carousel();
            //console.log('SHOULD BE REMOVED!');
            //animateCSS('#addm_frame', outanim).then((message) => {
                //$('#addpocket_modal').remove();
                //$('#uc').append(data['htm']);
                //refresh_carousel();
            //});
            /*$('#uc').append(data['htm']);
            refresh_carousel();*/
            }
            break;


        //pocket deleted successfully, refresh page! - DONE!
        case 149:{
            $('#'+data['pid']).remove();
            refresh_carousel();
            }
            break;


        //here is a transfer modal! - DONE
        case 151:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#addt_frame', inanim);
            /*$('#close_modal').click(function(){
                animateCSS('#addt_frame', outanim).then((message) => {
                $('#addtransfer_modal').remove();
                });
                });*/
            }
            break;


        //transfer registered, close the modal - DONE!
        case 152:{
            removeitem('addt_frame', 'addtransfer_modal')
            refresh_carousel();
            }
            break;


        //here is a category modal!
        case 161:{
            $('#pagecontent').append(data['htm']);
            animateCSS('#cat_frame', inanim)
            }
            break;


        //here is a modal frame where you can add or modify category, remove category_modal
        case 164:{
            animateCSS('#cat_frame', outanim).then((message) => {
                $('#category_modal').remove();
                $('#pagecontent').append(data['htm']);
                animateCSS('#addc_frame', inanim);
                }).then((message) =>
                 {
                    $('#add_category').click(function(){

                        if ( $('#hidden_id').attr('cid') ){
                            var id = $('#hidden_id').attr('cid');
                        }
                        else{
                            var id = false;
                        }

                        var type = $('#cat_type').is(':checked');

                        if (!$('#category_name').val()){
                            req_for_error('Category name must be set!');
                        }

                        else{
                            var name = $('#category_name').val();
                            var data= {event: 268, cid: id,  cname: name, type: type};
                            send_message('newmessage', data)
                        }

                    });

                    $('#cat_type').change(function(){
                    if(this.checked) {
                        $('#cat_span').removeClass("red")
                    }
                    else{
                        $('#cat_span').addClass("red")
                    }
                    });
                 });

            }
            break;


        //category deleted, remove from list - DONE
        case 162:{
            animateCSS( "#row_"+data['id'].toString() , removeanim ).then( (message) => $('#row_'+data['id']).remove() );
            }
            break;


        //category added or modified, remove addcategory modal and replace it with this
        case 169:{
            $('#addcategory_modal').remove();
            $('#pagecontent').append(data['htm']);
            animateCSS('#cat_frame', inanim);
            }
            break;


        //del this id row from page - DONE
        case 171:{
                $('#'+data['to_del']).remove();
            }
            break;
    }
});


function req_for_error(message){
    var data = {event: 291, message:message};
    send_message('newmessage', data);
};


function deluser(e){
        var data = {userid: e.id, event: 271};
        send_message('newmessage', data);
};


function addpocket(){
    var data = {event: 241};
    send_message('newmessage', data);
};


function addtransfer(type){
    var data = {event: 251, type: type, pocket: current_slide}
    send_message('newmessage', data);
};


function transfer(p, c, a, d){

    if (!a || isNaN(a)){
        var data ={event: 291, message:'Transfer amount must be numeric!'};
        send_message('newmessage', data);
        $('#transfer_amount').val('');
        return;
    };

    var data = {event: 252, pocketid: p, categoryid: c, amount: a, detail: d}
    send_message('newmessage', data);
    return;
};


function show_cat(){
    var data = {event: 261};
    send_message('newmessage', data);
};


function edit_cat(e){
    var data = {event: 263, id: e};
    send_message('newmessage', data);
};


function del_cat(e){
    var data = {event: 262, id: e};
    send_message('newmessage', data);
};


function add_cat(){
    var data = {event: 264};
    send_message('newmessage', data);
};


function submitform(form){
    $("#"+form.toString()).submit()
};


function delpocket(pocket_id){
    var data = {event: 242, p_id: pocket_id};
    send_message('newmessage', data);
};


function refresh_carousel(){
    var data = {event: 281, cs: current_slide};
    send_message('newmessage', data);
};


function show_loginmodal(){
    $("#loginmodal").show();
    animateCSS( "#login_frame" , inanim);
};


function show_signupmodal(){
    $("#signupmodal").show();
    animateCSS( "#signup_frame" , inanim);
};


function show_help(){
    //console.log('SHOW HELP MODAL!');
    var data = {event: 289};
    send_message('newmessage', data);
};


function show_resetp(){
    var data = {event: 288};
    send_message('newmessage', data);
};


function reset_p(){
    var p_o = $('#c_password').val();
    var p1 = $('#n_password1').val();
    var p2 = $('#n_password2').val();
    //send to 287
    if((!p_o||p_o=='')||(!p1||p1=='')||(!p2||p2=='')){
        req_for_error('All inputs must be set!');
        return;
    }
    var data = {event: 287, o_pw: p_o, n_pw1: p1, n_pw2: p2};
    send_message('newmessage', data);
    console.log('RESET PASSWORD');
};


function hideitem(item1, item2){
    animateCSS( "#"+item1.toString() , outanim).then((message) => {
        $( "#"+item2.toString()).hide();
        });
};


function removeitem(item1, item2){
    animateCSS( "#"+item1.toString() , outanim).then((message) => {
        $( "#"+item2.toString()).remove();
        });
};


function loginattempt(){
    var username = $('#login_username').val();
    var password = $('#login_password').val();
    var data = {event: 221, username: username, password: password};
    send_message('newmessage', data);
};


function signupattempt(){
    var username = $('#signup_username').val();
    var email = $('#signup_email').val();
    var password1 = $('#signup_password').val();
    var password2 = $('#signup_password2').val();
    var agreed = $('#signup_agree').is(':checked');

    var data = {event: 211, username: username, email:email, password1: password1, password2: password2, agreed: agreed};
    send_message('newmessage', data);
};


function uc_next(){
    $('#usercarousel').carousel('next');
};

function uc_prev(){
    $('#usercarousel').carousel('prev');
}


//animation handler
const animateCSS = (element, animation, prefix = 'animate__',) =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = document.querySelector(element);

    node.classList.add(`${prefix}animated`, animationName, 'animate__faster');

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd() {
      node.classList.remove(`${prefix}animated`, animationName);
      resolve('Animation ended');
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
  });
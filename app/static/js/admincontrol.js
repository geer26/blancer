function deluser(e){
        var data = {userid: e.id, event: 271};
        send_message('newmessage', data);
};


function revert_category(id){
    var data = {event: 272, cid: id};
    send_message('newmessage', data);
};


function hide_category(id){
    var data = {event: 273, cid: id}
    send_message('newmessage', data);
};


function del_category(id){
    var data = {event: 274, cid: id};
    send_message('newmessage', data);
};
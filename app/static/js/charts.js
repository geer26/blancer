var currentchart = 1;
var showed = 0


function fromtimestamp(str) {
    return new Date(str).getFullYear() + '-' + (new Date(str).getMonth()+1) + '-' + new Date(str).getDate();
};


function show_display(){
    if (showed==0){
        //slidedown();
        $('#showch').show();
        $('#showtr').hide();
        $('#switchbtn').html('show transfers')
    }
    else{
        //slideup();
        $('#showch').hide();
        $('#showtr').show();
        $('#switchbtn').html('show charts')
    }
};


function toTimestamp(date){
    return parseInt((new Date(date).getTime()).toFixed(0))
};


function setdates(min, max){

    var mindate = fromtimestamp(min);
    var maxdate = fromtimestamp(max);

    $('#startdate').val(mindate);
    $('#enddate').val(maxdate);

    $('#startdate').attr('min',mindate);
    $('#enddate').attr('min',mindate);
    $('#startdate').attr('max',maxdate);
    $('#enddate').attr('max',maxdate);

};


function newdates(min, max){

    var mindate = fromtimestamp(min);
    var maxdate = fromtimestamp(max);

    $('#startdate').val(mindate);
    $('#enddate').val(maxdate);

}


function upd(pid){
    var mintime = $('#startdate').val();
    var maxtime = $('#enddate').val();
    var mitime = toTimestamp(mintime);
    var matime = toTimestamp(maxtime);
    $('#startdate').attr('max',maxtime);
    $('#enddate').attr('min', mintime);
    var data ={event: 294, pid: parseInt(pid), mintime:mitime, maxtime:matime};
    send_message('newmessage', data);
};


function pagechart(){
    $('#'+currentchart.toString()).show();
};


function next_chart(){
    $('#'+currentchart.toString()).hide();
    (currentchart > charts.length-1) ? currentchart = 1 : currentchart ++;
    pagechart();
};


function prev_chart(){
    $('#'+currentchart.toString()).hide();
    (currentchart < 2) ? currentchart = charts.length : currentchart --;
    pagechart();
};


/*function upd_date(){
    console.log('Startdate: ', $('#startdate').val());
    console.log('End date: ', $('#enddate').val());
};*/


function slideup(){
    var charts = document.querySelector('#showch');
    var trs = document.querySelector('#showtr');
    var animation = setInterval(frame, 100);
    function frame() {
        if (charts.style.height <= 0) {  //animation ended
            //hide charts
            //show transfers
            $('#showch').hide();
            $('#showtr').show();
            $('#switchbtn').html('show charts')
            clearInterval(animation);
        } else {
            charts.style.height--;
        }
    }
};


function slidedown(){};
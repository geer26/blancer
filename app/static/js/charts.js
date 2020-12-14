var currentchart = 1;
var showed = 0


function fromtimestamp(str) {
    return new Date(str).getFullYear() + '-' + (new Date(str).getMonth()+1) + '-' + new Date(str).getDate();
};


function show_display(){
    if (showed==0){
        $('#showch').show();
        $('#showtr').hide();
        $('#switchbtn').html('show transfers')
    }
    else{
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


function upd_date(){
    console.log('Startdate: ', $('#startdate').val());
    console.log('End date: ', $('#enddate').val());
};
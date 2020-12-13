var currentchart = 1;


$('#startdate').click(function(date){
    upd_date();
    }
);


function timestamp(str) {
    return new Date(str).getFullYear() + '-' + new Date(str).getMonth() + '-' + new Date(str).getDate();
}


function setdates(min, max){
    console.log(timestamp(min));
    console.log(timestamp(max));
    $('#startdate').min = timestamp(min);
    $('#enddate').min = timestamp(max);
}


function pagechart(){
    //console.log( $('#'+ currentchart.toString()) );
    $('#'+currentchart.toString()).show();
}


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
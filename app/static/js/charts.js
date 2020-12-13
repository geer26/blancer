var currentchart = 1;


$('#startdate').datepicker({
            selectMonths: true, // Creates a dropdown to control month
            yearRange: 5, // Creates a dropdown of 10 years to control year,
            today: 'Today',
            close: 'Ok',
            closeOnSelect: true, // Close upon selecting a date
            autoClose: true,
            onSelect: upd_date('time')
        });


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


function upd_date(date){
    console.log(date);
};
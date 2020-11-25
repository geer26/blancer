var currentchart = 1;


function pagechart(){
    //console.log( $('#'+ currentchart.toString()) );
    $('#'+currentchart.toString()).show();
}


function timestamp(str) {
    return new Date(str).getTime();
}


function createslider(minmax) {

    var mintime = minmax['min'];
    var maxtime = minmax['max'];

    mit = parseInt(mintime);
    mat = parseInt(maxtime);

    var mindate = {
        year: new Date( mit ).getFullYear(),
        month: new Date( mit ).getMonth() + 1,
        day: new Date( mit ).getDate()
        };

    var maxdate = {
        year: new Date( mat ).getFullYear(),
        month: new Date( mat ).getMonth() + 1,
        day: new Date( mat ).getDate()
        };

    $('#sd').val(timestamp(mintime));
    $('#ed').val(timestamp(maxtime));

    document.getElementById("sd").min = mindate['year'] +'-'+mindate['month']+'-'+mindate['day'] ;
    document.getElementById("ed").max = maxdate['year'] +'-'+maxdate['month']+'-'+maxdate['day'] ;

    var options = {
        start: [timestamp(mintime), timestamp(maxtime)],
        connect: true,
        range: {
            'min': timestamp(mintime),
            'max': timestamp(maxtime)
        }
    };

    noUiSlider.create(slider, options);

    var fromdate = {
        year: new Date( parseInt(slider.noUiSlider.get()[0]) ).getFullYear(),
        month: new Date( parseInt(slider.noUiSlider.get()[0]) ).getMonth() + 1,
        day: new Date( parseInt(slider.noUiSlider.get()[0]) ).getDate()
        };

    var todate = {
        year: new Date( parseInt(slider.noUiSlider.get()[1]) ).getFullYear(),
        month: new Date( parseInt(slider.noUiSlider.get()[1]) ).getMonth() + 1,
        day: new Date( parseInt(slider.noUiSlider.get()[1]) ).getDate()
        };

    $('#sd').val( fromdate['year'] +'-'+fromdate['month']+'-'+fromdate['day'] );
    $('#ed').val( todate['year'] +'-'+todate['month']+'-'+todate['day'] );
    document.getElementById("sd").max = document.getElementById("ed").value;
    document.getElementById("ed").min = document.getElementById("sd").value;

};


function updslider(){

    var fromdate = {
        year: new Date( parseInt(slider.noUiSlider.get()[0]) ).getFullYear(),
        month: new Date( parseInt(slider.noUiSlider.get()[0]) ).getMonth() + 1,
        day: new Date( parseInt(slider.noUiSlider.get()[0]) ).getDate()
        };

    var todate = {
        year: new Date( parseInt(slider.noUiSlider.get()[1]) ).getFullYear(),
        month: new Date( parseInt(slider.noUiSlider.get()[1]) ).getMonth() + 1,
        day: new Date( parseInt(slider.noUiSlider.get()[1]) ).getDate()
        };

    $('#sd').val( fromdate['year'] +'-'+fromdate['month']+'-'+fromdate['day'] );
    $('#ed').val( todate['year'] +'-'+todate['month']+'-'+todate['day'] );
    document.getElementById("sd").max = document.getElementById("ed").value;
    document.getElementById("ed").min = document.getElementById("sd").value;
};


function setslider_from(){
    //set slider left side value
    slider.noUiSlider.set([timestamp($('#sd').val()), null]);
    //set enddate date input min value
    document.getElementById("ed").min = document.getElementById("sd").value;
};


function setslider_to(){
    //set slider right side value
    slider.noUiSlider.set([null, timestamp($('#ed').val())]);
    //set startdate date input max value
    document.getElementById("sd").max = document.getElementById("ed").value;
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
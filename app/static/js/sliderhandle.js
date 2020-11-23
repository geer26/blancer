
function timestamp(str) {
    return new Date(str).getTime();
}


function createslider(minmax){

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
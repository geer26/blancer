
function timestamp(str) {
    return new Date(str).getTime();
}


function createslider(minmax){

    var mintime = minmax['min'];
    var maxtime = minmax['max'];

    $('#sd').val(timestamp(mintime));
    $('#ed').val(timestamp(maxtime));

    var slider = document.querySelector('#rangeselector');

    var options = {
        start: [timestamp(mintime), timestamp(maxtime)],
        connect: true,
        range: {
            'min': timestamp(mintime),
            'max': timestamp(maxtime)
        }
    };

    noUiSlider.create(slider, options);

};


function updslider(target){
    console.log(target);
}
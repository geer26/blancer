//var pos_datapoints = [];
//var neg_datapoints = [];
//var dp = []
var d = []

function fix_point(amount, date, detail, category){
    d.push([date, amount]);
    //dp.push({x: date, y: amount, detail: detail, category: category});
    //(amount >= 0) ? pos_datapoints.push({x: date, y: amount, detail: detail, category: category}) : neg_datapoints.push({x: date, y: amount, detail: detail, category: category})

};


function chart_loaded(){
    console.log('HELLO!');



    var options = {

        chart: {
            type: 'bar'
        },

        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 3,
            opacity: 0.5
        },

        series: [{
            name: 'transfers',
            data: d
        }],

        xaxis: {
            labels: {
                datetimeFormatter: {
                year: 'yyyy',
                month: 'MMM \'yy',
                day: 'dd MMM',
                hour: 'HH:mm'
                }
            }
        }

    }

    var chart = new ApexCharts(document.querySelector("#chart"), options);

    chart.render();

};



var d = []
var pos_data = []
var neg_data = []
var index = 1;
var charts = [];

var pie_pos_amounts = []
var pie_pos_labels = []
var pie_neg_amounts = []
var pie_neg_labels = []

function fix_point(amount, date, detail, category){
    d.push([date, amount]);
    (amount > 0) ? pos_data.push([date, amount]) : neg_data.push([date, amount]);
};


function next_chart(){
    //console.log('NEXT');
    if (index == charts.length - 1){
        index = 0;
    } else{
        index++;
    }
    chart_loaded();
};


function prev_chart(){
    //console.log('PREV');
    if (index == 0){
        index = charts.length - 1;
    } else {
        index--;
    }
    chart_loaded();
};


function chart_loaded(){
    charts[index]();
};


function show_pies(){

    $('#chart').empty();

    var options = {
          series: [44, 55, 13, 43, 22],
          chart: {
          width: 380,
          type: 'pie',
        },

        labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],

        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();

};

charts.push(show_pies);


function show_bars(){

    //console.log('SHOW BARS');

    $('#chart').empty();

    var options = {

        colors : ['#24d900', '#ff0019'],

        chart: {
            type: 'bar',
            background: '#1976d2'
        },

        series: [
            {
            name: 'incomes',
            data: pos_data
            },
            {
            name: 'expenses',
            data: neg_data
            }
        ],

        yaxis: {
            labels: {
                formatter: function (value) {
                return value + "$";
                }
            }
        },

        xaxis: {
            labels: {
                /*formatter: function (value) {
                    var d = new Date(value);
                    var opts = {year: 'numeric', month: 'short', day: 'numeric'};

                    return d.toLocaleString('en-US',opts) // The formatter function overrides format property
                },*/
            }

        }

    }

    var chart = new ApexCharts(document.querySelector("#chart"), options);

    chart.render();
};

charts.push(show_bars);
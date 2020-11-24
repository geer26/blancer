//TODO delete this

var d = [];
var pos_data = [];
var neg_data = [];
var c_max = 0;
var c_min = 0;
var index = 0;
var charts = [];

var pie_pos_amounts = []
var pie_pos_labels = []
var pie_neg_amounts = []
var pie_neg_labels = []

function fix_point(amount, date, detail, category){
    d.push([date, amount]);
    (amount > 0) ? pos_data.push([date, amount]) : neg_data.push([date, amount]);
    if (amount>c_max){c_max=amount};
    if (amount<c_min){c_min=amount};

    if (amount > 0){  //pos transfers
        if (pie_pos_labels.indexOf(category) > -1){
            pie_pos_amounts[pie_pos_labels.indexOf(category)] += amount;
        }else{
            pie_pos_labels.push(category);
            pie_pos_amounts.push(amount);
        }
    }

    else{  //neg transfers
        if (pie_neg_labels.indexOf(category) > -1){
            pie_neg_amounts[pie_neg_labels.indexOf(category)] += Math.abs(amount);
        }else{
            pie_neg_labels.push(category);
            pie_neg_amounts.push(Math.abs(amount));
        }
    }



};


function next_chart1(){
    //console.log('NEXT');
    if (index == charts.length - 1){
        index = 0;
    } else{
        index++;
    }
    chart_loaded();
};


function prev_chart1(){
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


function show_bars(){

    //console.log('SHOW BARS');

    $('#chart').empty();

    var options = {

        colors : ['#24d900', '#ff0019'],

        dataLabels: {
            enabled: false
        },

        chart: {
            type: 'bar',
            height: '100%',
            background: 'rgba(0,0,0,.1)'
        },

        title: {
            text: 'All transfers',
            align: 'left',
            floating: false,
            style: {
                fontSize:  '14px',
                fontWeight:  'bold',
                color:  '#263238'
                },
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
            max: c_max,
            min: c_min,
            labels: {
                formatter: (value) => {
                return value + "$";
                }
            }
        },

        xaxis: {
            labels: {
                formatter: (value) => {
                    var d = new Date(value);
                    var opts = {year: 'numeric', month: 'short', day: 'numeric'};

                    return d.toLocaleString('en-US',opts) // The formatter function overrides format property
                },
            }

        }

    }

    var chart = new ApexCharts(document.querySelector("#chart"), options);

    chart.render();
};

charts.push(show_bars);


function show_pos_pies(){

    $('#chart').empty();

    var options = {
          series: pie_pos_amounts,
          chart: {
          height: '100%',
          type: 'donut',
          background: 'rgba(0,0,0,.1)'
        },

        title: {
            text: 'All incomes',
            align: 'left',
            floating: false,
            style: {
                fontSize:  '14px',
                fontWeight:  'bold',
                color:  '#263238'
                },
            },

        labels: pie_pos_labels,

        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              height: '70%'
            }
          }
        }]

        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();

};

charts.push(show_pos_pies);


function show_neg_pies(){

    $('#chart').empty();

    var options = {
          series: pie_neg_amounts,
          chart: {
          height: '100%',
          type: 'donut',
          background: 'rgba(0,0,0,.1)'
        },

        title: {
            text: 'All expenses',
            align: 'left',
            floating: false,
            style: {
                fontSize:  '14px',
                fontWeight:  'bold',
                color:  '#263238'
                },
            },

        labels: pie_neg_labels,

        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              height: '70%'
            }
          }
        }]

        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();

};

charts.push(show_neg_pies);
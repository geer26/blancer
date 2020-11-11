var pos_datapoints = [];
var neg_datapoints = [];

function fix_point(amount, date, detail, category){

    console.log(amount, ' : ', date, ' : ', detail, ' : ', category);

};


function chart_loaded(){
    console.log('HELLO');
    //showchart();
}


function showchart(){
    var dataPoints = [];
    var y = 0;
    var x = new Date(2016, 0, 02).getTime();
    var oneDayInms = (24 * 60 * 60 * 1000);

    var stockChart = new CanvasJS.StockChart("chartContainer",{
    title:{
        text:"Detailed transfers"
    }
    });
    stockChart.render();
};
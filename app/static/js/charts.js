var pos_datapoints = [];
var neg_datapoints = [];
var dp = []

function fix_point(amount, date, detail, category){
    dp.push({x: date, y: amount, detail: detail, category: category});
    (amount >= 0) ? pos_datapoints.push({x: date, y: amount, detail: detail, category: category}) : neg_datapoints.push({x: date, y: amount, detail: detail, category: category})

};


function chart_loaded(){
    console.log('HELLO!');
}


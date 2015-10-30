var rowClasses = ['#00CC99', '#74FFFF'];

$('document').ready(function(){
    readData('').success(generateTable);
});

var readData = function(path){
    return $.ajax({
        url: '/read/' + path,
        method: 'get'
    });
};

var generateTable = function(json){
    var data = JSON.parse(json);
    var table = $('#table tbody');
    for(var i in data){
        var row = $('<tr></tr>').attr('bgcolor',rowClasses[i%2]);
        row.append($('<td></td>').addClass('col-md-1').text(data[i]['type']));
        row.append($('<td></td>').text(data[i]['name']));
        row.append($('<td></td>').text(data[i]['user']));
        row.append($('<td></td>').text(data[i]['right']));
        table.append(row);
    }
};
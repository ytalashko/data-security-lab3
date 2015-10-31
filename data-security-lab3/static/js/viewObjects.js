//todo: improve color map
var rowClasses = ['#00CC99', '#74FFFF'];

var path = '';

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
        var isFile = data[i]['type']==='f';
        var row = $('<tr></tr>').attr('bgcolor',rowClasses[i%2]);
        row.append($('<td></td>').append( $('<span></span>').addClass('glyphicon')
                .addClass(isFile?'glyphicon-file':'glyphicon-folder-open')
        ).addClass('col-md-1'));
        row.append($('<td></td>').text(data[i]['name']));
        row.append($('<td></td>').text(data[i]['user']));
        row.append($('<td></td>').text(data[i]['right']));
        table.append(row);
    }
};
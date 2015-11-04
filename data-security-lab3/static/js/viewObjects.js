//todo: improve color map
var rowClasses = ['#DADEE0', '#FFFFFF'];
var isRoot = true;

$('document').ready(function(){
    readRequest('').success(generateTable);
    $('#breadcrumb li a').on('click', function(){
        goBack($(this).data('path'));
    });
    $('#logoutLink').click(function(){
        $.ajax({
            url: '/logout/'
        }).success(function(data){
            if(data==='true')
                window.location.href = '/';
            else{
                alert('cannot logout');
            }
        }).error(function () {
            alert('something goes wrong');
        });
    });
    initModalHandlers();

    setInterval(function () {
        $.get('/x/').success(function (captcha) {
            var captchaText = 'please enter captcha: F(' + captcha + ') = ?';
            var result = prompt(captchaText);
            $.post('/check-captcha/', {y: result}, function (res) {
                if (res !== 'true') {
                    $.get('/logout/');
                    window.location.href = '/';
                }
            });
        });
    }, 5000);
});



var generateTable = function(json){
    var data = JSON.parse(json);
    var table = $('#table tbody');
    table.empty();
    if(!isRoot){
        var row = $('<tr></tr>');
        row.append($('<td></td>').addClass('glyphicon').addClass('glyphicon-level-up'));
        row.append($('<td></td>').append($('<a></a>').text('Go back ..')
            .on('click', function(){ goBack();})).css('cursor', 'pointer'));
        table.append(row);
    }
    for(var i in data){
        var isFile = data[i]['type']==='f';
        var row = $('<tr></tr>').attr('bgcolor',rowClasses[i%2]);
        row.append($('<td></td>').append( $('<span></span>').addClass('glyphicon')
                .addClass(isFile?'glyphicon-file':'glyphicon-folder-open')
        ).addClass('col-md-1'));
        var link = $('<a></a>').attr('data-path',data[i]['name'])
            .attr('data-type',isFile).text(data[i]['name'])
            .on('click',function(){
                goNext($(this).data('path'), $(this).data('type'));
            }).css('cursor', 'pointer');
        row.append($('<td></td>').append(link));
        row.append($('<td></td>').text(data[i]['user']));
        row.append($('<td></td>').text(data[i]['right']));
        var actionTd = $('<td></td>');
        var deleteButton = $('<div></div>').addClass('btn').addClass('btn-default')
            .append($('<span></span>').addClass('glyphicon').addClass('glyphicon-remove'))
            .append('Delete').attr('data-toggle','modal').attr('data-target','#deleteModal')
            .attr('data-path',getCurrentPath() + data[i]['name'] + '/');
        var writeButton = $('<div></div>').addClass('btn').addClass('btn-default')
            .append($('<span></span>').addClass('glyphicon').addClass('glyphicon-edit'))
            .append('Write').attr('data-toggle','modal')
            .attr('data-path',getCurrentPath() + data[i]['name'] + '/');
        if(isFile){
            writeButton.attr('data-target','#writeFileModal');
        } else {
            writeButton.attr('data-target','#writeDirModal');
        }
        var executeButton = $('<div></div>').addClass('btn').addClass('btn-default')
            .append($('<span></span>').addClass('glyphicon').addClass('glyphicon-search'))
            .append('Execute').on('click',exec);
        actionTd.append(deleteButton);
        actionTd.append(writeButton);
        actionTd.append(executeButton);
        row.append(actionTd);
        table.append(row);
    }
};

var goNext = function(path, fileType){
    if(path==='') isRoot = true;
    path = getCurrentPath() + path + '/';
    if(fileType){
        openFile(path);
        //breadcrumbGoNext(path);
    } else {
        openDir(path);
        breadcrumbGoNext(path);
    }
};

var goBack = function(path){
    if(typeof(path) === 'undefined')
        openDir(breadcrumbGoBack());
    else {
        breadcrumbGo(path);
        openDir(path);
    }
};

var openDir = function(dirPath){
    readRequest(dirPath).success(generateTable).error(function(){
        alert('error');
    });
};

var openFile = function(filePath){
    alert('file: ' + filePath)
};

var breadcrumbGoNext = function(path){
    isRoot = false;
    var temparr = path.split('/');
    var shortPath = temparr[temparr.length-2];
    $('#breadcrumb').append($('<li></li>')
            .append($('<a></a>').attr('data-path',path).text(shortPath)
            .on('click',function(){
                goBack($(this).data('path'));
            }).css('cursor', 'pointer')));
};

var breadcrumbGoBack = function(){
    if(isRoot) return;
    $('#breadcrumb li:last-child').remove();
    var element = $('#breadcrumb li:last-child')
    var path = element.find('a').data('path');
    if(path==='') isRoot = true;
    return path;
};

var breadcrumbGo = function(path){
    if(path!=='') {
        var realPath = path.split('/');
        var items = $('#breadcrumb li').has('a[data-path*='+realPath[realPath.length-2]+']');
        items.slice(1,items.length).each(function(){ $(this).remove()});
    } else {
        $('#breadcrumb li:gt(0)').each(function(){ $(this).remove()});
        isRoot = true;
    }
};

//action methods
var del = function (path) {
    deleteRequest(path).success(function(data){
        $('#errorModal').modal('show');
    });
};
var exec = function () {
    alert('execute object action');
};
var write = function () {

};

//request functions
var readRequest = function(path){
    return $.ajax({
        url: '/read/' + (path == '' ? '/':path),
        method: 'get'
    });
};
var writeRequest = function(path, data){
    return $.ajax({
        url: '/write/' + (path == '' ? '/':path),
        method: 'post',
        data: data
    });
};
var executeRequest = function(path){
    return $.ajax({
        url: '/execute/' + (path == '' ? '/':path),
        method: 'get'
    });
};
var deleteRequest = function(path){
    return $.ajax({
        url: '/delete/' + (path == '' ? '/':path),
        method: 'get'
    });
};

//utils functions
var getCurrentPath = function(){
    return $('#breadcrumb li:last-child a').data('path');
};

var initModalHandlers = function(){
    $('#deleteModal').on('show.bs.modal', function (e) {
        var button = $(e.relatedTarget);
        var filename = button.data('path').split('/').slice(-2)[0];
        $('#deleteModal .modal-title').text('Delete: ' + filename);
        deleteRequest(button.data('path')).success(function(data){
            if(data === 'true') {
                $('#deleteModal .modal-body').text('Sucessfully deleted');
                $('tr').has('td').has('a[data-path='+filename+']').remove();
            } else
                $('#deleteModal .modal-body').text('Error deleting item. Check rights');
        });
    });
    $('#writeFileModal').on('show.bs.modal', function(e){
        var button = $(e.relatedTarget);
        var path = '/write/' + button.data('path');
        var filename = path.split('/').slice(-2)[0];
        $('#writeFileModal .modal-title').text('Write data to ' + filename);
        $('#writeFileForm').submit(function () {
            $.post(path, $(this).serialize(), function(result){
                if(result === 'true'){
                    alert("Successful!!");
                } else
                    alert("Error!");
                $('#writeFileModal').modal('hide');
            }, 'json');
        })
    });
};
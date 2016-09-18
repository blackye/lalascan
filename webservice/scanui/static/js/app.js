jobList = null;

function readableTime(seconds) {
    if(isNaN(seconds)){
        return "-";
    }
    day = Math.floor(seconds / 86400);
    hour = Math.floor((seconds - day * 86400) / 3600);
    minute = Math.floor((seconds - day * 86400 - hour * 3600 ) / 60);
    second = seconds - day * 86400 - hour * 3600 - minute * 60
    if(hour < 10){
        hour = "0" + hour;
    }
    if(minute < 10){
        minute = "0" + minute;
    }
    if(second < 10){
        second = "0" + second;
    }
    if(day == 0){
        return hour + ":" + minute + ":" + second;
    }else{
        return day + "d " + hour + ":" + minute + ":" + second;
    }
}

function percentFormat(number) {
    if(isNaN(number)){
        return "-";
    }
    number = number * 100;
    var percent =number.toFixed(2);
    return percent+"%";
}

template.helper('percentFormat', percentFormat);

template.helper('readableTime',readableTime);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


function showAllJobs(){
   $.get("api/jobs", function(result){
        jobList = result;
        $("#tableBody").empty();
        $.each(result,function(n,value) {
           var data = {job: value, index:n}
           var html = template('jobRow', data);
           $("#tableBody").append(html);
        });
    });
}


function getJobOptions(){
    var aj = $.ajax( {
        url:'/api/jobs',
        type:'options',
        cache:false,
        dataType:'json',
        success:function(data) {
            $("#selectWhiteListFile").empty();
            $("#selectWhiteListFile").append(template('fileOption', {file:{value:null,display_name:''}}))
            $("#selectBlackListFile").empty();
            $("#selectBlackListFile").append(template('fileOption', {file:{value:null,display_name:''}}))
            console.log("options success")
            console.log(data)
            whiteList = data.actions.POST.white_list_file.choices
            $.each(whiteList,function(n,file) {
               var data = {file: file}
               var html = template('fileOption', data);
               $('#selectWhiteListFile').append(html);
            });
            blackList = data.actions.POST.black_list_file.choices
            $.each(blackList,function(n,file) {
               var data = {file: file}
               var html = template('fileOption', data);
               $('#selectBlackListFile').append(html);
            });
        },
        error : function(request) {
            var data = eval('(' + request.responseText + ')');
            alert(data.detail);
         }
    });
}


$('#newJobModal').on('show.bs.modal',
function(event) {
 getJobOptions();
});

$('#newJobModal').on('hide.bs.modal',
function(event) {
});


function createJob(){
    var csrftoken = getCookie('csrftoken');
    $("#createJobButton").addClass('disabled');
    $.ajax({
        cache: true,
        type: "POST",
        url:'/api/jobs/',
        headers:{'X-CSRFToken':csrftoken},
        data:$('#newJobForm').serialize(),
        async: true,
        success: function(data) {
            $("#createJobButton").removeClass('disabled');
            $('#newJobModal').modal('hide');
            showAllJobs();
        },
        error: function(request) {
            $("#createJobButton").removeClass('disabled');
            console.log(request)
            var data = eval('(' + request.responseText + ')');
            for(var key in data){
                alert(key+':'+data[key])
            }
        }
    });
}

function deleteJob(url){
    var csrftoken = getCookie('csrftoken');
    var aj = $.ajax( {
        url:url,
        type:'DELETE',
        data:$('#deleteJobForm').serialize(),
        headers:{'X-CSRFToken':csrftoken},
        async: true,
        cache:false,
        dataType:'json',
        success:function(data) {
            console.log(data)
            $('#deleteJobModal').modal('hide');
            showAllJobs();
        },
        error : function(request) {
            console.log(request)
            var data = eval('(' + request.responseText + ')');
            alert(data.detail);
         }
    });
}


function showDeleteJobModal(url){
     $('#deleteJobModal').modal('show');
     $('#deleteButton').attr('onclick',"deleteJob('"+url+"')");
}

function showLog(id){
    $('#logModal').modal('show');
    url = '/static/' + id + '/job.log';
    $('#logContainer').empty();
    var aj = $.ajax( {
        url:url,
        type:'GET',
        cache:false,
        dataType:'text',
        success:function(data) {
            console.log(data)
            $('#logContainer').append(data);
        },
        error : function(request) {
            console.log(request)
            $('#logContainer').append("Get log failed");
         }
    });
}

function updateJobStatus(){
    $.get("api/jobs", function(result){
        jobList = result;
        $.each(result,function(n,job) {
            id = job.id;
            nameId = "#"+id+"-name";
            progressId = "#" + id + "-progress";
            statusId = "#" + id + "-status";
            hitId = "#" + id + "-hit";
            hitRateId = "#" + id + "-hitRate";
            leftId = "#" + id + "-left";
            logId = "#" + id + "-log";
            downloadId = "#" + id + "-download";
            operationId = "#" + id+ "-operation";
            $(nameId).html(job.name);
            $(progressId).attr("style", "width: "+job.percent_complete+"%");
            $(progressId).attr("aria-valuenow", job.percent_complete);
            if(job.status == 1){
                $(progressId).addClass("active");
                $(leftId).html(readableTime(job.time_remaining));
            }else{
                $(progressId).removeClass("active");
                $(leftId).html("-");
            }
            if(job.status==0){
                $(logId).attr("disabled", "disabled");
                $(downloadId).attr("disabled", "disabled");
                $(downloadId).attr("href", "#");
            }else{
                $(logId).removeAttr("disabled");
                $(downloadId).removeAttr("disabled");
                $(downloadId).attr("href", "/static/"+job.id+"/output.txt");
            }
            if(job.status == 1){
                $(operationId).attr("class", "glyphicon glyphicon-pause");
                $(operationId).attr("onclick", "createCommand('"+job.url+"', 0)");
            }else if(job.status== 4){
                $(operationId).attr("class", "glyphicon glyphicon-play");
                $(operationId).attr("onclick", "createCommand('"+job.url+"', 1)");
            }else{
                $(operationId).attr("class", "glyphicon glyphicon-repeat");
            }
            var data = {status:job.status}
            var html = template('statusTemplate', data);
            $(statusId).html(html);
            $(hitId).html(job.recv_success_total);
            $(hitRateId).html(percentFormat(job.recv_success_total/job.sent_total));
        });
    });
}

function createCommand(job_url, cmd){
    var csrftoken = getCookie('csrftoken');
    data = {'job':job_url, cmd:cmd}
    var aj = $.ajax( {
        url:'/api/commands/',
        type:'POST',
        data: data,
        headers:{'X-CSRFToken':csrftoken},
        async: true,
        cache:false,
        dataType:'json',
        success:function(data) {

        },
        error : function(request) {
            console.log(request)
            var data = eval('(' + request.responseText + ')');
            alert(data.detail);
         }
    });
}

function autoUpdateStatus(time){
    updateJobStatus();
    setTimeout("autoUpdateStatus("+time+")", time )
}

$(document).ready(function(){
    showAllJobs();
    autoUpdateStatus(1000);
});
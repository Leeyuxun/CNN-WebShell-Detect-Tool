//初始化
$(function () {
    console.log('%c                                 \n' +
        '     /\\                          \n' +
        '    /  \\   _ __ ___   __ _ _ __  \n' +
        '   / /\\ \\ | \'_ ` _ \\ / _` | \'_ \\ \n' +
        '  / ____ \\| | | | | | (_| | | | |\n' +
        ' /_/    \\_\\_| |_| |_|\\__,_|_| |_|\n' +
        '                                 \n' +
        '%c我是一匹狼，仰望着星空却找不到月亮','color:#f00','color:#ff5990');
    toastr.options = {
        timeOut: 2000,
        positionClass: "toast-top-center",
        progressBar: true,
        showMethod: "slideDown",
        hideMethod: "slideUp",
        messageClass: 'toast-message',
        closeHtml: '<button type="button">&times;</button>',
        showDuration: 200,
        hideDuration: 200
    };
    let theme=$.cookie('theme');
    if(theme=="dark"){
        $("body").addClass('dark');
        $("#theme").addClass('text-warning');
        $("#theme").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');
    }else{
        $("body").removeClass('dark');
        $("#theme").removeClass('text-warning');
        $("#theme").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');
    }
    return false;
});




/**index 首页**/
//签到规则
$("#getCheckinRule").click(function () {
   let modal=$("#checkinRuleModal");
   if(modal.find('.modal-body').html()==""){
       Ajax("/index/getCheckinRule",'get','',function (res) {
           modal.find('.modal-body').html(res.data)
           modal.modal('show');
       });
   }else{
       modal.modal('show');
   }
});
//签到
$("#checkin").click(function () {
    let modal=$("#checkinModal");
    if(modal.find('.modal-body').html()==""){
        Ajax("/user/checkin",'get','',function (res) {
            let html='';
            let total=parseInt($(".checkin-total").html())+1;
            let div='<button class="btn-rounded btn btn-secondary btn-pulse disabled del"><del>已签到</del></button>';
            $("#checkin-status").html(div);
            $(".checkin-total").html(total);
            $(".checkin-num").html("连续签到 "+res.data.count+" 天");
            html+='<div class="text-center">' +
                '恭喜您获得：<span class="text-warning font-weight-bold"> '+res.data.coin+' </span>金币<br>' +
                '已连续签到：<span class="text-warning font-weight-bold"> '+res.data.count+' </span>天' +
                '</div>';
            modal.find('.modal-title').html(res.msg);
            modal.find('.modal-body').html(html);
            modal.modal('show');
        });
    }else{
        modal.modal('show');
    }
});

/**评论*/
$(".comments").on('click',".commentSubmit",function (event) {
    let form=$(this).parents("form");
    if(form[0].checkValidity()==false){
        form.addClass("was-validated");
    }else{
        let data=form.serialize();
        Ajax(comment_url,'post',data,function (res) {
            swal(res.msg, '', "success").then(function () {
                location.reload()
            });
        });
    }
    return false;
});

$(".comments .commentReply").on('click',function () {
    let p=$(this).parents(".comment-tools");
    let form=p.siblings('.commentForm');
    if(form.length>0){
        form.remove();
    }else{
        $(".comments .media .commentForm").remove();
        let id=$(this).data('id');
        let html='' +
            '<form class="input-group m-t-10 commentForm"  novalidate>\n' +
            '   <input type="text" name="content" class="form-control" placeholder="说点什么吧" value="" required="">\n' +
            '   <input type="hidden" name="reply_id" value="'+id+'">' +
            '   <div class="input-group-append">\n' +
            '       <button type="button" class="btn btn-primary commentSubmit">回复</button>\n' +
            '  </div>\n' +
            '</form>';
        p.after(html);
    }
});
$(".comments .commentLike").on('click',function () {
    let id=$(this).data('id');
    let that=this;
    Ajax('/api/addLike','POST',{id:id},function (res) {
        let num=parseInt($(that).find("span").html());
        if(res.data.status==1){
            $(that).addClass("text-primary");
            $(that).find("span").html(num+1);
        }else{
            $(that).removeClass("text-primary");
            $(that).find("span").html(num-1);
        }
    });
});
$(".comments .commentDel").on('click',function () {
    swal({
        title: "提示",
        text: "确定要删除该评论吗？",
        icon: "warning",
        buttons: true,
    }).then((y) => {
        if (y) {
            let id=$(this).data('id');
            Ajax('/api/delComment','POST',{id:id},function (res) {
                $("#comment-"+id).prev("hr").remove();
                $("#comment-"+id).remove();
            });
        }
    });

});

/**公共**/

$("#theme").click(function () {
    let theme=$.cookie('theme');
    if(theme!="dark"){
        $.cookie('theme','dark',{  expires: 7,path: '/' });
        $("body").addClass('dark');
        $(this).addClass('text-warning');
        $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');
    }else{
        $.removeCookie('theme');
        $.removeCookie('theme',{  expires: 7,path: '/' });
        $("body").removeClass('dark');
        $(this).removeClass('text-warning');
        $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');
    }
    return false;
});
$("form.needs-validation").on('submit',function (e) {
    e.preventDefault();
    e.stopPropagation();
    let form=$(this)[0];
    if(form.checkValidity()==false){
        $(this).addClass("was-validated");
    }
});
//ajax
function Ajax(url,type,data,success,com=null,error2=null) {
    $.ajax({
        url:url,
        headers: {'X-CSRF-TOKEN': $.cookie('X-CSRF-TOKEN')},
        type:type,
        data:data,
        success:function (res) {
            if(res.code==1){
                success(res)
            }else{
                toastr.warning(res.msg||"未知错误");
            }
        },
        error:function () {
            toastr.error("Server Error");
            if(error2!=null)
                error2
        },
        complete:function (res) {
            if(com !=null)
                com(res)
        }
    })
}
function getObjectURL(file) {
    var url = null ;
    if (window.createObjectURL!=undefined) { // basic
        url = window.createObjectURL(file) ;
    } else if (window.URL!=undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file) ;
    } else if (window.webkitURL!=undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file) ;
    }
    return url ;
}
// 时间戳转多少分钟之前
function getDateDiff(dateTimeStamp){
    var minute = 1000 * 60;
    var hour = minute * 60;
    var day = hour * 24;
    var month = day * 30;
    var now = new Date().getTime();
    var diffValue = now - dateTimeStamp;
    if(diffValue < 0){return;}
    var monthC =diffValue/month;
    var weekC =diffValue/(7*day);
    var dayC =diffValue/day;
    var hourC =diffValue/hour;
    var minC =diffValue/minute;
    if(monthC>=1){
        result="" + parseInt(monthC) + "月前";
    }
    else if(weekC>=1){
        result="" + parseInt(weekC) + "周前";
    }
    else if(dayC>=1){
        result=""+ parseInt(dayC) +"天前";
    }
    else if(hourC>=1){
        result=""+ parseInt(hourC) +"小时前";
    }
    else if(minC>=1){
        result=""+ parseInt(minC) +"分钟前";
    }else
        result="刚刚";
    return result;
}
function getDateTimeStamp(dateStr){
    return Date.parse(dateStr.replace(/-/gi,"/"));
}

function goBack(){
    if ((navigator.userAgent.indexOf('MSIE') >= 0) && (navigator.userAgent.indexOf('Opera') < 0)){ // IE
        if(history.length > 0){
            window.history.go( -1 );
        }else{
            window.opener=null;window.close();
        }
    }else{ //非IE浏览器
        if (navigator.userAgent.indexOf('Firefox') >= 0 ||
            navigator.userAgent.indexOf('Opera') >= 0 ||
            navigator.userAgent.indexOf('Safari') >= 0 ||
            navigator.userAgent.indexOf('Chrome') >= 0 ||
            navigator.userAgent.indexOf('WebKit') >= 0){

            if(window.history.length > 1){
                window.history.go( -1 );
            }else{
                window.opener=null;window.close();
            }
        }else{ //未知的浏览器
            window.history.go( -1 );
        }
    }
}
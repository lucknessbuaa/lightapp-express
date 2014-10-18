$(function() {
    var phoneValidator = /^\d{11}$/;
    $("#submitButton").bind("click", function() {
        if ($("#company").val() == "0") {
            alert("请选择快递公司");
            return;
        };
        if ($("#name").val() == "") {
            alert("请输入收件人姓名");
            return;
        };
        if ($("#phone").val() == "") {
            alert("请输入收件人手机号");
            return;
        };
        if ($("#destination").val() == "") {
            alert("请输入收件人宿舍地址");
            return;
        };


        var data = $("#signup").serialize();

        data += "&type=0";
        if ($('#fast').is(":checked")) {
            data += "&fast=1";
        } else {
            data += "&fast=0";
        }

        $("#submitButton").html("正在提交...");
        $('#submitButton').prop('disabled', true);
        $.post("/app/send/add", data, 'json').then(function(json) {
            if (json.ret_code == 0) {
                $('div.well').html('<p><b>订单已提交成功！</b></p> <p>您可以在 <a href="profile">个人中心</a> 标签页下的链接 <br><a href="recent">我的订单</a> 中跟踪您的订单处理状态</p>' + '<br><p class="tips"><b>目前</b>代领订单有三种状态:</p>' + '<p><span class="label" style="background-color:#999">处理中</span>&nbsp;&nbsp;<span class="tips">已收到您的订单,正在处理中</span></p>' + '<p><span class="label label-info">已取件,待配送</span>&nbsp;&nbsp;<span class="tips">已领到快递,等待送到宿舍</span></p>' + '<p><span class="label label-success">已完成</span>&nbsp;&nbsp;<span class="tips">订单已送达完成</span></p>');
            }else if(json.ret_code == 1002) {
                alert('请到个人中心完善个人资料！');
            }else {
                alert(json.msg);
            }
        }, function() {
            alert('网络异常！');
        }).always(function(){
            $("#submitButton").html("提交订单");
            $('#submitButton').prop('disabled', false);
        });
    });

    $(".feeRule-link").bind("click", function() {
        $('#price-modal').modal({
            backdrop: true,
            keyboard: true,
            show: true
        });
    });
});

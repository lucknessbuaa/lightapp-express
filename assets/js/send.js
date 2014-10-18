$(function() {
    var $form = $('form');
    var form = $form[0];
    $form.submit(function(e) {
        e.preventDefault();

        $('#submitButton').html('正在提交...');
        $('#submitButton').prop('disabled', true);
        $.post('/app/send/add', {
            company: form.company.value,
            fetchdate: form.fetchdate.value,
            fetchperiod: form.fetchperiod.value,
            type: 1,
            notes: form.notes.value
        }, 'json').then(function(data) {
            if (data.ret_code === 1001) {
                return alert(data['msg'])
            }else if(data.ret_code === 1002) {
                return alert('请到个人中心完善个人资料！');
            }else if(data.ret_code === 0){
				$('div.container').html('<p><b>订单已提交成功！</b></p> <p>您可以在 <a href="profile">个人中心</a> 标签页下的链接 <br><a href="recent">我的订单</a> 中跟踪您的订单处理状态</p>'
						+ '<br><p class="tips"><b>目前</b>代寄订单有三种状态:</p>'
						+ '<p><span class="label" style="background-color:#999">处理中</span>&nbsp;&nbsp;<span class="tips">已收到您的订单,正在处理中</span></p>'
						+ '<p><span class="label label-info">已收件,待寄出</span>&nbsp;&nbsp;<span class="tips">已上门收件,等待寄出</span></p>'
						+ '<p><span class="label label-success">已完成</span>&nbsp;&nbsp;<span class="tips">订单已寄送完成</span></p>'						
				);
            }
            
            $('#submitButton').html('提交订单');
            $('#submitButton').prop('disabled', false);

        }, function() {
            alert('网络异常');
        });
    });
});

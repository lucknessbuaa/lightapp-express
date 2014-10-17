$(function() {
    var $form = $('form');
    var form = $form[0];
    $form.submit(function(e) {
        e.preventDefault();

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
            }

            window.location.reload();
        }, function() {
            alert('网络异常');
        });
    });
});

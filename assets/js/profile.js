$(function() {
    var $form = $('form');
    var form = $form[0];
    $form.submit(function(e) {
        e.preventDefault();

        $.post('/app/profile', {
            schoolid: this.schoolid.value,
            campusid: this.campusid.value,
            name: this.name.value,
            gender: $('input[name="gender"]:checked').val(),
            susheid: this.address.value,
            phone: this.phone.value
        }, 'json').then(function(data) {
            if (data.ret_code === 1001) {
                return alert('操作失败');
            }

            if (data.points_got) {
                alert('恭喜您获得了200积分！');
            }
            window.location.reload();
        }, function() {
            alert('网络异常');
        });
    });
});

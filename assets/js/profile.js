$(function() {
    var $form = $('form');
    var $submit = $form.find('input[type=submit]');
    var form = $form[0];
    var phoneValidator = /^\d{11}$/;
    $form.submit(function(e) {
        e.preventDefault();

        if (form.name.value == "") {
            return alert("请输入姓名");
        }

        if (form.phone.value == "") {
            return alert("请输入手机号码");
        }

        if (form.address.value == "") {
            return alert("请输入宿舍地址");
        }

        if (!phoneValidator.test(form.phone.value)) {
            return alert("请输入正确格式的手机号码 : )");
        }

        $submit.button('loading');
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
        }).always(function() {
            $submit.button('reset');
        });
    });
});

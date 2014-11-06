$(function() {
    $('.orders form').submit(function(e) {
        e.preventDefault();

        if (this.price.value === '') {
            return alert('价格不能为空！');
        }

        if (isNaN(parseFloat(this.price.value))) {
            return alert('价格格式不对！');
        }

        $('input[type=submit]').button('loading');
        $.post('/mgr/api/sign/complete', {
            id: this.id.value,
            price: this.price.value
        }, 'json').then(function() {
            alert('操作成功！');
            window.location.reload();
        }, function() {
            alert('操作失败！');
        }).always(function() {
            $('input[type=submit]').button('reset');
        });
    });
});

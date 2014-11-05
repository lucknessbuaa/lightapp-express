$(function() {
    $('.orders form').submit(function(e) {
        e.preventDefault();

        if (this.order_no.value === '') {
            return alert('快递单号不能为空');
        }

        $('input[type=submit]').button('loading');
        $.post('/mgr/api/send/complete', {
            id: this.id.value,
            order_no: this.order_no.value
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
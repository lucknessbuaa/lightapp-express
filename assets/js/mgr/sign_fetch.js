$(function() {
    $('.orders form .refuse').click(function(e) {
        e.preventDefault();
        $('.orders form .refuse').button('loading');

        $.post('/mgr/api/sign/refuse', {
            id: $('.orders form input[name=id]').val(),
        }, 'json').then(function() {
            alert('操作成功!');
            window.location.reload();
        }, function() {
            alert('操作失败!');
        }).always(function() {
            $('.orders form .refuse').button('reset');
        });
    });

    $('.orders form').submit(function(e) {
        e.preventDefault();

        $('input[type=submit]').button('loading');
        $.post('/mgr/api/sign/receive', {
            id: this.id.value,
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

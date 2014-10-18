$(function() {
    $(".deletePackage").bind("click", function(){
        var value = $(this.parentElement.parentElement).find('input[name=orderid]').val();

        $(this).html('正在删除...');
        $(this).prop('disabled', true);
        $.post("/app/recent/delete",{
            orderid: parseInt(value)
        }, 'json').then(function(data){
            if(data.retValue.code === 200){
                alert('该订单成功删除！');
            }else if(data.retValue.code === 405) {
                alert('该订单不存在或已被取消!');
            }else if(data.retValue.code === 500) {
                alert('错误，用户不存在或者authcode对应的用户与订单id对应的用户不一致');
            }else if(data.retValue.code === 710) {
                alert('该订单已被处理，无法删除');
            }else {
                alert('未知错误！');
            }

            window.location.reload();
        }, function() {
            alert('网络异常');
        }).always(function() {
            $(this).html('删除');
            $(this).prop('disabled', false);
        }); 
    });
});

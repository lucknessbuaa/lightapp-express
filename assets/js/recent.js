$(function() {
    $(".btn.deletePackage").bind("click", function(){
        var value = $(this.parentElement.parentElement).find('input[name=orderid]').val();

        $.post("/app/recent/delete",{
            orderid: parseInt(value)
        }, function(data){
            if(data.ret_code == 0){
                alert('该订单成功删除！');
            }

            window.location.reload();
        }, 'json'); 
    });
});

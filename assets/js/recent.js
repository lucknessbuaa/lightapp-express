$(function() {
    $(".btn.delete-sign").bind("click", function(){
        $(".btn.delete-sign").html("正在删除...");
        $(".btn.delete-sign").prop('disabled', true);

        $.post("/app/recent/delete",{
        }, function(data){
            if(data.ret_code == 0){
                alert('该订单成功删除！');
            }

            window.location.reload();
        }, 'json'); 
    }, this);

    $(".btn.delete-send").bind("click", function(){
        $(".btn.delete-send").html("正在删除...");
        $(".btn.delete-send").prop('disabled', true);

        $.post("/app/recent/delete",{
        }, function(data){
            if(data.ret_code == 0){
                alert('该订单成功删除！');
            }

            window.location.reload();
        }, 'json'); 
    }, this);
});

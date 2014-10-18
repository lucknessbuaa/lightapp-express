$(function(){
	var num = 1;
	var points = $('#points').data('points');
	$('#buy-btn').click(function(e){
		$('#order-modal-num').html(num);
		$('#order-modal-points').html(num*points);
		$('body').prepend($("<div class='mask' style='background-color:rgba(0,0,0,0.5);height:"+$(document).height()+"px;width:100%;position:absolute;left:0;top:0'></div>"));
		$('#order-modal').show();
	});
	$('#cancel-submit').click(function(){$('#order-modal').hide();$('.mask').remove();});
	$('#submit-btn').bind("click",function(e){
		var that = this;
		if($("#name").val()=="" || $("#phone").val()=="" || $("#destination").val()==""){
			alert("请输入完整的收货人信息");
			return;
		}
		var data = $("#order-info-form").serialize();
		data += ("&num="+num)
		//alert(data);
		$(this).html("正在提交...");
	    $(this).prop('disabled',true);
	    $.post("order",data,function(json){
			if(json.code==200){
				$('.modal-body').html('<p><b>订单已提交成功！</b></p> <p>请耐心等待我们上门配送商品</p> <p><span id="count-down-sec">3</span>秒后将跳转回积分商城首页...</p>');
				setInterval(function(){$('#count-down-sec').html($('#count-down-sec').html()-1)}, 950);
				setTimeout(function(){ window.location.href="/"}, 3000);
			}else {
	            alert(json.msg);
			}
	        $(that).html("提交订单");
	        $(that).prop('disabled',false);

		},"json");
	});

	function addNum(i){
		if(num+i<1){
			return;
		}
		num+=i;
		$('.numcart .numb .numb-int').html(num);
		$('.prototal .total-int').html(num*points);
	}
	$('.minus').click(function(){
		addNum(-1);
	});
	$('.plus').click(function(){
		addNum(1);
	});
});
(function($$){
	
	$$.init();
	
	var dataAreaVm = new Vue({
		el:'#data-area',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			
			/***
			 * 
			 */
			revoke: function(item) {
				console.log(item.name)
				
				var  postdata = {}
				postdata.id = item.id;
					
				app.fillToken(postdata);
				
				$$.ajax({
		            type: "post",
					url: urls.url_invokeStock,
					data:postdata,
		            timeout: 3000,
		            success: function(data) {
		            	console.log("success:" + urls.url_getMyStocks);
		            	
		            	if(data['errcode'] != 0){
		            		plus.nativeUI.toast(data['errmsg']);
		            		return;
		            	}else if(data['errcode'] == 0) {
		            		plus.nativeUI.toast("撤單成功！");
		            		return;
		            	}
		            },
		            error: function(xhr, type, errorThrown) {
		                plus.nativeUI.toast(errorThrown);
		            }
		        });// ajax
			}
		}
	});
	
	$$.plusReady(function(){
		console.log("rebackStock plusReady.");
	});
	
	function cb_getStockList(data){
		
		for(var it in data) {
			if(data[it].type==1) {
				data[it].type = "買入";
			}else if(data[it].type==2) {
				data[it].type = "賣出";
			}else {
				
			}
//			console.log(data[it].price);
//			console.log(data[it].amount);
//			console.log(data[it].volume);
		}
		
		console.log(JSON.stringify(data))
		dataAreaVm.datas = data;
	};
	
	function getStockList(){
		var  postdata = {}
					
		app.fillToken(postdata);
		postdata.ext = 'unfinished';   // 所有未完成的交易記錄
		
		$$.ajax({
            type: "get",
			url: urls.url_getTradeHistory,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + urls.url_getMyStocks);
            	
            	if(data['errcode'] != 0){
            		plus.nativeUI.toast(data['errmsg']);
            		return;
            	}
            	
            	cb_getStockList(data.retdata);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	window.addEventListener('display', function(){
		console.log("reback stock page display.");
		
		getStockList();
	});
	
	window.addEventListener('reset', function(){
		console.log("reback stock page reset.");
	});
	
})(mui);

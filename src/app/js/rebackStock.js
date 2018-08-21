(function($$){
	
	$$.init();
	var param = {};
	
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
				
				var url = urls.url_invokeStock;
				var  postdata = {}
				postdata.id = item.id;
					
				app.fillToken(postdata);
				
				if(param.contestid != undefined) {
					url = urls.url_contestStockInvoke;
					postdata.contestid = param.contestid;
				}
				
				$$.ajax({
		            type: "post",
					url: url,
					data:postdata,
		            timeout: 3000,
		            success: function(data) {
		            	console.log("success:" + url);
		            	
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
		
		var url = urls.url_getTradeHistory;
		if(param.contestid != undefined) {
			url = urls.url_contestHistoryList;
			postdata.cid = param.contestid;    // 附帶比賽id 參數
		}
		
		$$.ajax({
            type: "get",
			url: url,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + url);
            	
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
	
	window.addEventListener('display', function(event){
		param = event.detail.data || {};
		console.log("reback stock page display.:" + JSON.stringify(param));
		
		getStockList();
	});
	
	window.addEventListener('reset', function(){
		console.log("reback stock page reset.");
	});
	
})(mui);

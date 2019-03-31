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
			}
		}
	});
	
	$$.plusReady(function(){
		console.log("history lsit  plusReady.");
	});
	
	function cb_getStockList(data){
		
		for(var it in data) {
			/***
			 * 類型
			 */
			if(data[it].type==1) {
				data[it].type = "買入";
			}else if(data[it].type==2) {
				data[it].type = "賣出";
			}else {
				
			}
			
			/***
			 * 狀態
			 */
			if(data[it].status==0) {
				data[it].status = "待成交";
			}else if(data[it].status==1) {
				data[it].status = "已完成";
			}else if(data[it].status==2){
				data[it].status = "撤單";
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
		app.fillRn(postdata);
		postdata.ext = 'all';   // 所有未完成的交易記錄
		
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
	
	window.addEventListener('display', function(event){
		param = event.detail.data || {};
		console.log("history lsit page display.:" + JSON.stringify(param));
		
		getStockList();
	});
	
	window.addEventListener('reset', function(){
		console.log("history lsit page reset.");
	});
	
})(mui);

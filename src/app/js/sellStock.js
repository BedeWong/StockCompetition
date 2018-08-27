

(function($$){
	
	// 父頁面傳送過來的參數
	var param = {}
	
	// 點擊股票 可以賣出、跳轉到交易頁面
	var pg_trade =  $$.noop;
	
	/***
	 * 跳轉到交易頁面
	 * @param {Object} item：
	 * 			item.uid 用戶
	 * 			item.code  股票代碼
	 * 			item.name  股票名字
	 * 			item.type  買入/賣出
	 */
	function toTrade(item){
		
		item.type = 'sale';   // 賣出
		if(param.contestid != undefined) {
			item.contestid = param.contestid;
		}
		
		mui.fire(pg_trade,'display',{data:item});
		//打开個股詳情
		mui.openWindow({
			id:'trade'
		});
	}
	
	var list_data = new Vue({
		el:'#list-data',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			
			tradeDetail:function(item){
				toTrade(item);
			}
		}
		
	});
	
	/**
	 * 獲取持倉股票信息成功后的回掉，在這個函數裏獲取股票的 現價等信息
	 * @param {Object} data
	 */
	function cb_getStockList(data){
		var code_lst = [];
		
		for(var it in data) {
			code_lst.push('s_' + data[it].code);
			console.log(data[it].code);
		}
		
		if(code_lst.length == 0) {
			return ;
		}
		
		hq_obj.get_hq_stock(function(rdat){
			rdat = rdat.replace(/[\r\n]/g, "");
			console.log(rdat);
			eval(rdat);
			
			for(var it in data) {
				var hq = eval('hq_str_s_' + data[it].code);
				
				hq = JSON.stringify(hq).split(',');
				data[it].cur_price = hq[1];          // 現價
				data[it].change_per = hq[3];          // 漲跌幅
			}
				
			//test
//			for(var it in data){
//				console.log(it + ': ' + JSON.stringify(data[it]) );
//			}
			
			// 賦值數據到模型
			list_data.datas = data;
		}, code_lst);
	};
	
	function getStockList(){
		var  postdata = {}
					
		app.fillToken(postdata);
		
		$$.ajax({
            type: "get",
			url: urls.url_getMyStocks,
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
	
	$$.plusReady(function(){
		
		pg_trade = mui.preload({
			url:"trade.html",
			id:"trade",//默认使用当前页面的url作为id
		});
		
	});
	
	window.addEventListener('display', function(event){
		param = event.detail.data || {};
		console.log("sell stock page display.:" + JSON.stringify(param))
		getStockList();
	});
	
})(mui);

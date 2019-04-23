(function($$){
	// 買入按鈕點擊 跳轉到此頁面
	var pg_myfavoritestock = $$.noop;
	
	// 賣出按鈕點擊 跳轉到此頁面
	var pg_sell =  $$.noop;
	
	// 撤單按鈕點擊跳轉到此頁面
	var pg_reback = $$.noop;
	
	// 成交記錄按鈕點擊 跳轉到此頁面
	var pg_historytrade = $$.noop;
	
	// 點擊股票 可以賣出、跳轉到交易頁面
	var pg_trade =  $$.noop;
	
	
	$$.plusReady(function(){
		
		pg_myfavoritestock = mui.preload({
			url:"myfavoritestock.html",
			id:"myfavoritestock",//默认使用当前页面的url作为id
		});
		
		pg_sell = mui.preload({
			url:"sellStock.html",
			id:"sellstock",//默认使用当前页面的url作为id
		});
		
		pg_reback = mui.preload({
			url:"rebackStock.html",
			id:"rebackStock",//默认使用当前页面的url作为id
		});
		
		pg_historytrade = mui.preload({
			url:"historytradelist.html",
			id:"historytradelist",//默认使用当前页面的url作为id
		});
		
		pg_trade = mui.preload({
			url:"trade.html",
			id:"trade",//默认使用当前页面的url作为id
		});
	});
	
	/**
	 * 買入按鈕點擊跳轉到這個頁面！！
	 */
	function toFavoriteStockPage(){
		mui.fire(pg_myfavoritestock,'display',{});
		//打开個股詳情
		mui.openWindow({
			id:'myfavoritestock'
		});
	};
	
	/**
	 * 跳轉到 賣出頁面展示可賣出的股票列表
	 */
	function toSellStock(){
		mui.fire(pg_sell,'display',{});
		//打开個股詳情
		mui.openWindow({
			id:'sellstock'
		});
	}
	
	/**
	 * 跳轉到撤單頁面，展示 買入/賣出 但還未成交的列表。
	 */
	function toRebackStock(){
		mui.fire(pg_reback,'display',{});
		//打开個股詳情
		mui.openWindow({
			id:'rebackStock'
		});
	}
	
	/**
	 * 跳轉到 成交記錄頁面你， 展示成功的歷史交易
	 */
	function toHistoryStockList(){
		mui.fire(pg_historytrade,'display',{});
		//打开個股詳情
		mui.openWindow({
			id:'historytradelist'
		});
	}/**   end  plusReady ***/
	
	/***************************************event*********************************************/
	/******
	 * 按鈕綁定事件：
	 */
	$$('#stock-buy')[0].addEventListener('tap', function(ev){
		console.log("買入按鈕點擊。");
		
		toFavoriteStockPage();
	});
	
	$$('#stock-sale')[0].addEventListener('tap', function(ev){
		console.log("賣出按鈕點擊。");
		
		toSellStock();
	});
	
	$$('#stock-reback')[0].addEventListener('tap', function(ev){
		console.log("撤單按鈕點擊。");
		
		toRebackStock();
	});
	
	$$('#stock-history')[0].addEventListener('tap', function(ev){
		console.log("成交歷史記錄按鈕點擊。");
		
		toHistoryStockList();
	});
	
	/******		******		******			******
	 * 持倉信息展示
	 */
	
	function toTrade(item){		
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
			
			/****
			 * 點擊買入
			 * @param {Object} item
			 */
			buyStock:function(item){
				console.log("買入 " + item.name);
				
				item.type = 'buy';
				toTrade(item);
			},
			
			/***
			 * 點擊賣出
			 * @param {Object} item
			 */
			saleStock:function(item) {
				console.log("賣出 " + item.name);
				
				item.type = 'sale';   // 賣出
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
			code_lst.push(data[it].code);
			console.log(data[it].code);
		}
		
		if(code_lst.length == 0) {
			return;
		}
		
		hq_obj.get_hq_stock(function(rdat){
			rdat = rdat.replace(/[\r\n]/g, "");
			console.log(rdat);
			eval(rdat);
			
			for(var it in data) {
				var hq = eval('hq_str_' + data[it].code);
				
				hq = JSON.stringify(hq).split(',');
				data[it].cur_price = parseFloat(hq[3]).toFixed(2);          // 現價
				data[it].change_per = parseFloat((hq[1] - hq[2]) / hq[2]*100).toFixed(2);          // 漲跌幅
				data[it].yingkui = parseFloat(data[it].cur_price - data[it].price).toFixed(2);   // 浮動盈虧
				data[it].mv = data[it].cur_price * data[it].count;                // 總市值
				data[it].allcount = data[it].count + data[it].freeze;       // 縂持倉數（T+1規則）
			}
				
			//test
			for(var it in data){
				console.log(it + ': ' + JSON.stringify(data[it]) );
			}
			
			// 賦值數據到模型
			list_data.datas = data;
			console.log(JSON.stringify(data));
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
	
	window.addEventListener('display', function(){
		console.log("mystockPosition html display.");
		
		getStockList();
	});
	
	
	window.addEventListener('show', function(){
		console.log("mystockPosition html show.");
	});
	
})(mui);

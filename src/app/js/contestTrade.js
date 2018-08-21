
(function($$){	
	$$.init();
	
	var wt = {};

	var mask=mui.createMask();//遮罩层
	
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
	
	var param = {}
	
	var user_info = new Vue({
		el:'#userinfo',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			}
		}
	});
	
	var stock_list = new Vue({
		el:'#user-stocks',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			buy : function(item){
				item.type = 'buy';
				item.contestid = item.cid;
				toTrade(item);		
			},
			sale : function(item){		
				console.log(JSON.stringify(item));
				
				item.type = 'sale';
				item.contestid = item.cid;
				toTrade(item);	
			}
		}
	});
	
	/***
	 * 根據獲取到的股票獲取其行情數據：最新價等數據
	 * @param {Object} data：a list  
	 */
	function get_stock_hq(data){
		lst = []
		for (var it in data) {
			lst.push(data[it].code);
		}
		
		if(lst.length == 0) {
			wt.close();
			return ;
		}
		
		console.log(JSON.stringify(lst));
		
		hq_obj.get_hq_stock(function(resp){
			eval(resp);
			
			for(var it in lst) {
				var hq_str = eval('hq_str_' + lst[it]);
//				console.log(hq_str);
				
				arr = hq_str.split(',');
				data[it]['cur_price'] = arr[3];
			}
			
			console.log(JSON.stringify(data));
            stock_list.datas = data;
            mask.close();
            wt.close();
		}, lst);
	}
	
	function get_user_stock(){
		var postdata = {}
		
		app.fillToken(postdata);
		app.fillRn(postdata);
		postdata.cid = param.id;
		
		mask.show();
		// 加載動畫
		wt = plus.nativeUI.showWaiting();
		$$.ajax({
            type: "get",
			url: urls.url_listContestUserStocks,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + urls.url_listContestUserStocks);
            	
            	if(data['errcode'] != 0){
            		plus.nativeUI.toast(data['errmsg']);
            		return;
            	}
            	
            	console.log(JSON.stringify(data['retdata']))
            	
            	get_stock_hq(data['retdata']);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	// 獲取用戶的本場比賽的基本信息
	function get_contest_user_info(){
		var postdata = {}
		
		app.fillToken(postdata);
		postdata.cid = param.id;
		
		$$.ajax({
            type: "get",
			url: urls.url_contestUserInfo,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + urls.url_contestUserInfo);
            	
            	if(data['errcode'] != 0){
            		plus.nativeUI.toast(data['errmsg']);
            		return;
            	}
            	
            	console.log(JSON.stringify(data['retdata']))
            	user_info.datas = data['retdata'];
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	
	
	$$.plusReady(function(){
		mask.show();
		
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
		
		mask.close();
	});
	
	/**
	 * 買入按鈕點擊跳轉到這個頁面！！
	 */
	function toFavoriteStockPage(){
		var dat = {};
		dat.contestid = param.id;
		mui.fire(pg_myfavoritestock,'display',{data:dat});
		//打开個股詳情
		mui.openWindow({
			id:'myfavoritestock'
		});
	};
	
	/**
	 * 跳轉到 賣出頁面展示可賣出的股票列表
	 */
	function toSellStock(){
		var dat = {};
		dat.contestid = param.id;
		mui.fire(pg_sell,'display',{data:dat});
		//打开個股詳情
		mui.openWindow({
			id:'sellstock'
		});
	}
	
	/**
	 * 跳轉到撤單頁面，展示 買入/賣出 但還未成交的列表。
	 */
	function toRebackStock(){
		var dat = {};
		dat.contestid = param.id;
		mui.fire(pg_reback,'display',{data:dat});
		//打开個股詳情
		mui.openWindow({
			id:'rebackStock'
		});
	}
	
	/**
	 * 跳轉到 成交記錄頁面你， 展示成功的歷史交易
	 */
	function toHistoryStockList(){
		var dat = {};
		dat.contestid = param.id;
		mui.fire(pg_historytrade,'display',{data:dat});
		//打开個股詳情
		mui.openWindow({
			id:'historytradelist'
		});
	}
	
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
	
	function toTrade(item){		
		mui.fire(pg_trade,'display',{data:item});
		//打开個股詳情
		mui.openWindow({
			id:'trade'
		});
	}
	
	window.addEventListener('display', function(event){
		param = event.detail.data;    // 父頁面傳送過來的數據.
		
		console.log(JSON.stringify(param));
		
		get_contest_user_info();
		get_user_stock();
	});
})(mui);

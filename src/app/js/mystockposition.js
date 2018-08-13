(function($$){
	// 買入按鈕點擊 跳轉到此頁面
	var pg_myfavoritestock = $$.noop;
	
	// 賣出按鈕點擊 跳轉到此頁面
	var pg_sell =  $$.noop;
	
	// 撤單按鈕點擊跳轉到此頁面
	var pg_reback = $$.noop;
	
	// 成交記錄按鈕點擊 跳轉到此頁面
	var pg_historytrade = $$.noop;
	
	
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
	
})(mui);

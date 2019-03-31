(function($$){
	console.log("indexDetail.js");
	
	var img_baseurl = 'http://image.sinajs.cn/newchart/';
	
	mui("#container-6").on('tap', ".tab-chart", function(ev){
		var id = this.getAttribute("id");
		var targetdiv = NaN;
		
		console.log(id);
		
		switch(id){
			case "tab-min":
				targetdiv = $("#chart-min");
				
				var imgurl = img_baseurl+"min/n/" + pramaData.symbol + '.gif';
				mui("#img-min")[0].setAttribute('src', imgurl);
				
				break;
			case "tab-day":
				targetdiv = $("#chart-day");
				
				var imgurl = img_baseurl+"daily/n/" + pramaData.symbol + '.gif';
				console.log(imgurl);
				mui("#img-day")[0].setAttribute('src', imgurl);
				break;
			case "tab-week":
				targetdiv = $("#chart-week");
				mui("#img-week")[0].setAttribute('src', img_baseurl+"weekly/n/" + pramaData.symbol + '.gif');
				break;
			case "tab-month":
				targetdiv = $("#chart-month");
				mui("#img-month")[0].setAttribute('src', img_baseurl+"monthly/n/" + pramaData.symbol + '.gif');
				break;
		}
		
		if (targetdiv == NaN) return;
		
		targetdiv.removeClass("mui-hidden").siblings().addClass("mui-hidden");
		$(this).addClass("tab-chart-cur").siblings().removeClass('tab-chart-cur');   // 當前點擊tab標簽
	});
	
	// 點擊買入 跳轉到交易頁面
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
		
		item.type = 'buy';   // 買入
		
		//test
		console.log(JSON.stringify(item));
		
		mui.fire(pg_trade,'display',{data:item});
		//打开個股詳情
		mui.openWindow({
			id:'trade',
			extras:{
				data:item  //扩展参数
			}
		});
	}

	mui('#stock-buy')[0].addEventListener('tap', function(ev){
		console.log("購買按鈕點擊。");
		
		var arg = {}
		app.fillToken(arg)
		arg.code = pramaData.symbol;
		arg.name = pramaData.name;
		arg.contestid = pramaData.contestid;
		
		toTrade(arg);
	});
	
	mui('#stock-add2favorite')[0].addEventListener('tap', function(ev){
		console.log("添加到自選股。");
		
		var  postdata = {}
					
		app.fillToken(postdata);
		
		postdata['code'] = pramaData.symbol;
		postdata['name'] = pramaData.name;
		postdata['uid'] = app.getState().uid;
		
//		for(var it in postdata) {
//			console.log(it + " : " + postdata[it]);
//		}
		
		mui.ajax({
            type: "post",
			url: urls.url_addStock2Favorite,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:addStock2Favorite");
            	
            	if(data['errcode'] == 0){
            		plus.nativeUI.toast(data['errmsg']);
            	} else {
            		plus.nativeUI.toast(data['errmsg']);
            	}
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	});
	
	mui('#stock-chat')[0].addEventListener('tap', function(ev){
		console.log("聊股按鈕點擊。");
	});
	
	
	$$.plusReady(function(){
		console.log("stock detail page plusReady.");
		pg_trade = mui.preload({
			url:"trade.html",
			id:"trade",//默认使用当前页面的url作为id
		});
	});
})(mui);

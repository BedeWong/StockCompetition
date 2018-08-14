(function($$){
	
	$$.plusReady(function(){
		console.log("Trade page ready.");
		
	});
	
	var dataAreaVm = new Vue({
		el:'#data-area',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			buy:function(it){
				console.log(JSON.stringify(it))
				
			},
			sale:function(it){
				console.log(JSON.stringify(it))
			}
		}
	});
	
	var dataCache = {}
	var b_price_box = false;   // 頁面加載價格框不出現值問題
	function updataData(){		
		hq_obj.get_hq_stock(function(retdata){
			retdata = retdata.replace(/[\r\n]/g, "");
			console.log(retdata);
			eval(retdata);
			
			var stockData = JSON.stringify(eval("hq_str_" + dataCache.code)).split(',');
			
			dataCache.jinkai = parseFloat(stockData[1]).toFixed(2);    // 今開
			dataCache.cur_price = parseFloat(stockData[3]).toFixed(2);  // 現價
			dataCache.zuoshou = parseFloat(stockData[2]).toFixed(2);  // 作收
			dataCache.change_per = ((dataCache.cur_price - stockData[2]) / stockData[2]*100).toFixed(2); // 34  漲幅
			
			dataCache.sale1_c = parseFloat(stockData[20]).toFixed(0);
			dataCache.sale1 = parseFloat(stockData[21]).toFixed(2);
			dataCache.sale2_c = parseFloat(stockData[22]).toFixed(0);
			dataCache.sale2 = parseFloat(stockData[23]).toFixed(2);
			dataCache.sale3_c = parseFloat(stockData[24]).toFixed(0);
			dataCache.sale3 = parseFloat(stockData[25]).toFixed(2);
			dataCache.sale4_c = parseFloat(stockData[26]).toFixed(0);
			dataCache.sale4 = parseFloat(stockData[27]).toFixed(2);
			dataCache.sale5_c = parseFloat(stockData[28]).toFixed(0);
			dataCache.sale5 = parseFloat(stockData[29]).toFixed(2);
			
			dataCache.buy1_c = parseFloat(stockData[10]).toFixed(0);
			dataCache.buy1 = parseFloat(stockData[11]).toFixed(2);
			dataCache.buy2_c = parseFloat(stockData[12]).toFixed(0);
			dataCache.buy2 = parseFloat(stockData[13]).toFixed(2);
			dataCache.buy3_c = parseFloat(stockData[14]).toFixed(0);
			dataCache.buy3 = parseFloat(stockData[15]).toFixed(2);
			dataCache.buy4_c = parseFloat(stockData[16]).toFixed(0);
			dataCache.buy4 = parseFloat(stockData[17]).toFixed(2);
			dataCache.buy5_c = parseFloat(stockData[18]).toFixed(0);
			dataCache.buy5 = parseFloat(stockData[19]).toFixed(2);
			
			if(!b_price_box){
				b_price_box = true;
				document.getElementById("price-box").value = dataCache.cur_price;
			}
			
			dataAreaVm.datas = dataCache;
		}, [dataCache.code,])
	};
	
	window.addEventListener('display', function(event){
		console.log(JSON.stringify(event.detail.data));
		
		dataCache = event.detail.data;
		updataData();
		
		if(dataCache.type == 'buy') {
			$("#button-buy").removeClass("mui-hidden");
			$("#button-sale").addClass("mui-hidden");
		}else if(dataCache.type == 'sale') {
			$("#button-sale").removeClass("mui-hidden");
			$("#button-buy").addClass("mui-hidden");
		}
		
		/*****
		 * 買入、賣出確認按鈕。
		 */
		mui('#stock-buy')[0].addEventListener('tap', function(event){
			console.log(document.getElementById("price-box").value);
			
			dataCache.price = $('#price-box').val();
			dataCache.count = $('#price-count').val();
			dataCache.vol = (dataCache.price*dataCache.count).toFixed(2);
			var charge = (dataCache.vol * 0.00025).toFixed(2);
			if(charge < 5) {
				charge = 5;
			}
			
			console.log("price:" + dataCache.price + ", count:"+ dataCache.count + ", vol:" + dataCache.vol + ", charge:" + charge);
			
			$('#box-stock-price')[0].innerText = "委托價：" + dataCache.price;
			$('#box-stock-count')[0].innerText = "賣出 " + dataCache.count + " 股";
			$('#box-stock-vol')[0].innerText = "成交金額：" + dataCache.vol;
			$('#box-stock-charge')[0].innerText = "手續費：" + charge.toFixed(2);
			
			$('#mark-box').removeClass('mui-hidden');
		});
		
		mui('#stock-sale')[0].addEventListener('tap', function(event){
			console.log(document.getElementById("price-count").value);
			
			dataCache.price = $('#price-box').val();
			dataCache.count = $('#price-count').val();
			dataCache.vol = (dataCache.price*dataCache.count).toFixed(2);
			var charge = dataCache.vol * 0.00025;
			if(charge < 5) {
				charge = 5;
			}
			
			console.log("price:" + dataCache.price + ", count:"+ dataCache.count + ", vol:" + dataCache.vol + ", charge:" + charge);
			
			$('#box-stock-price')[0].innerText = "委托價：" + dataCache.price;
			$('#box-stock-count')[0].innerText = "賣出 " + dataCache.count + " 股";
			$('#box-stock-vol')[0].innerText = "成交金額：" + dataCache.vol;
			$('#box-stock-charge')[0].innerText = "手續費：" + charge.toFixed(2);
			
			$('#mark-box').removeClass('mui-hidden');
		});
		
		/****
		 * 確定買入
		 */
		mui('#box-stock-ok')[0].addEventListener('tap', function(event){
			$('#mark-box').addClass('mui-hidden');
			
			console.log("委托下單確認：" + dataCache.name);
			
			var url;
			var postdata = {}
			
			if (dataCache.type == 'buy'){
				url = urls.url_buystock;
			}else if(dataCache.type == 'sale'){
				url = urls.url_salestock;
			}
			
			postdata.code = dataCache.code;
			postdata.name = dataCache.name;
			postdata.price = dataCache.price;
			postdata.amount = dataCache.count;
			
			app.fillToken(postdata);   // uid & token
			
			mui.ajax({
	            type: "post",
				url: url,
				data:postdata,
	            timeout: 3000,
	            success: function(data) {
	            	console.log("success:股票購買：" + postdata.code + ", " + postdata.name);
	            	
	            	if(data['errcode'] == 0){
	            		plus.nativeUI.toast("委托成功!");
	            	} else {
	            		plus.nativeUI.toast(data['errmsg']);
	            	}
	            },
	            error: function(xhr, type, errorThrown) {
	                plus.nativeUI.toast(errorThrown);
	            }
	        });// ajax
		});
		
		/**
		 * 取消買
		 */
		mui('#box-stock-cancel')[0].addEventListener('tap', function(event){
			$('#mark-box').addClass('mui-hidden');
			
		});
		
		window.addEventListener('refresh', function(event){
			console.log("mui-back,  關閉！");
			
			dataAreaVm.resetData();
			$('#mark-box').addClass('mui-hidden');
		});
		
//		setInterval(updataData, 5000);
	});
	
})(mui);

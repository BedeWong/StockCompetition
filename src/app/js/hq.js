
(function($$, obj){
	
	/***
	 * 板塊列表、分類列表
	 */
	obj.url_FLJK = 'http://money.finance.sina.com.cn/q/view/newFLJK.php?param=';
	
	/***
	 * 漲跌榜接口
	 */
	obj.url_RANKLIST = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?sort=changepercent&node=hs_a&asc=0&num=100&page=1';
	
	/***
	 * 個股行情，指數行情數據
	 */
	obj.url_HQSTOCK = 'http://hq.sinajs.cn/';
	
	/***
	 * 獲取個股内外盤盤口數據
	 */
	obj.url_STOCKDATA = 'https://hq.sinajs.cn/etag.php';
	
	/***
	 * 獲取個股公告
	 */
	obj.url_NOTICEDATA = 'http://vip.stock.finance.sina.com.cn/api/jsonp.php/var%20noticeData=/CB_AllService.getMemordlistbysymbol';
	
	/***
	 * 獲取個股公告，新聞
	 */
	obj.url_NEWSDATA = 'http://news.sinajs.cn/rn=&maxcnt=20&dcnt=10&list=';
	
	/***
	 * 獲取成分股股數
	 */
	obj.url_HQNODEDATA_COUNT = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=';
	
	/****
	 * 獲取板塊成分股、指數成分股
	 */
	obj.url_HQNODEDATA = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=100&sort=symbol&asc=1&node=';
	
	/****
	 * 獲取個股逐筆交易數據，
	 * trade_INVOL_OUTVOL : 内盤外盤數據
	 */
	obj.url_HQSTOCK_TRANLIST = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=1&symbol=';
	
	/***
	 * 根据id获取对应的
	 */
	obj.id2IndexhqMap = {
		sh50index:{name:"上證指數",reqcode:"s_sh000001",code:"sh000001"},
		szindex:{name:"深證指數",reqcode:"s_sz399001",code:"sz399001"},
		secondboardindex:{name:"創業板指",reqcode:"s_sz399006", code:"sz399006"},
		hs300index:{name:"滬深300指數",reqcode:"s_sh000300", code:"sh000300"}
	};
	obj.id2IndexDetailMap = {
		sh50index:{name:"上證指數",reqcode:"sh000001",code:"sh000001"},
		szindex:{name:"深證指數",reqcode:"sz399001",code:"sz399001"},
		secondboardindex:{name:"創業板指",reqcode:"sz399006", code:"sz399006"},
		hs300index:{name:"滬深300指數",reqcode:"sh000300", code:"sh000300"}
	};
	
	/***
	 *  獲取板塊數據
	 */
	obj.get_FLJK_class = function(cb){
		var url = this.url_FLJK + 'class';
		console.log(url);
		
		$.ajax({
		    type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'script',
			success: function(data) {
				console.log("success:get_FLJK_class");
				
				var ret = JSON.stringify(S_Finance_bankuai_class).match(/{".*"}/);
				ret = ret.length ? JSON.parse(ret[0]) : "";
				
				for(var it in ret) {
					var lst = ret[it];
					lst = lst.split(',');
					ret[it] = lst;
				}
				
				cb(ret);
			},
			error: function(xhr, type, errorThrown) {
				console.log("error:get_FLJK_class");
				console.log(type);
				console.log(errorThrown);
				plus.nativeUI.toast(errorThrown);
			}
		});
	},
	
	obj.get_FLJK_industry = function(cb){
		var url = this.url_FLJK + 'industry';
		console.log(url);
		
		 $.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'script',
            success: function(data) {
            	console.log("success:get_FLJK_industry");
            	 
            	var ret = JSON.stringify(S_Finance_bankuai_industry).match(/{".*"}/);
				ret = ret.length ? JSON.parse(ret[0]) : "";
				
				for(var it in ret) {
					var lst = ret[it];
					lst = lst.split(',');
					ret[it] = lst;
				}
				
            	cb(ret);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	obj.get_FLJK_area = function(cb){
		var url = this.url_FLJK + 'area';
		console.log(url);
		
		 $.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'script',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_FLJK_area");
            	console.log(data);
            	var dict = eval("S_Finance_bankuai_area");
            	var ret = {};
				
				for(var it in dict) {
					var lst = dict[it];
					lst = lst.split(',');
					ret[it] = lst;
				}
            	cb(ret);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	
	/***
	 *  獲取漲跌榜數據
	 * @param {Object} asc： 0 升序， 1降序
	 */
	obj.get_rank_list_data = function(cb, asc){
		var url = this.url_RANKLIST;
		if(asc == 1) {
			url = url.replace(/asc=0/g, 'asc=1');
		}
		console.log("get_rank_list_data:");
		console.log(url);
		
		 $.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'text',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_rank_list_data");
//          	console.log(JSON.stringify(data));
            	var obj = eval(data);
            	cb(obj);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 獲取指數詳情
	 * lst 指數
	 */
	obj.get_hq_index = function(cb, lst){
		var url = obj.url_HQSTOCK + "rn=" + (new Date()).valueOf() + "&list=" + lst.join(',');
		
		console.log(url);
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'text',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_hq_index");
//          	var obj = eval(data);
            	cb(data);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 
	 * 獲取個股實時行情
	 */
	obj.get_hq_stock = function(cb, lst){
		var url = obj.url_HQSTOCK + "rn=" + (new Date()).valueOf() + "&list=" + lst.join(',');
		
		console.log(url);
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'script',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_hq_stock");
//          	var obj = eval(data);
            	cb(data);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 獲取個股公告
	 */
	obj.get_notice_data = function(cb, code) {
		var url = obj.url_NEWSDATA + code + ',gg_' + code + ",ntc_" + code;
		url = url.replace(/rn=/g, 'rn='+(new Date()).valueOf());
		console.log(url);
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'script',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_notice_data");
            	cb(data);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 獲取板塊成分股、指數成分股
	 * @page: 頁數
	 * @nod: 數據節點如：zhishu_000001表示上證指數
	 * 					gn_bdgn表示百度概念
	 */
	obj.get_bankuai_stocklist = function(cb, page, nod){
		if(page < 1) return "";
		if(nod.trim() == "") return "";
		
		var url = obj.url_HQNODEDATA + nod;
		url = url.replace(/page=1/g, 'page=' + page);
		
		console.log(url);
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'text',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_bankuai_stocklist");
            	console.log(data);
            	          	
            	cb(eval(data));
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 獲取板塊、指數的成分股數量
	 */
	obj.get_bankuai_stockcount = function(cb, nod) {
		var url = obj.url_HQNODEDATA_COUNT + nod;
		console.log(url);
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'text',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_bankuai_stocklist");
            	console.log(data);
   	
            	cb(eval(data));
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	},
	
	/***
	 * 獲取個股逐筆交易數據：
	 * @param {Object} cb  回掉函數
	 * @param {Object} code  股票代碼
	 * @param {Object} num  條數
	 * 
	 */
	obj.get_stock_tradeList = function(cb, code, num){
		var url = obj.url_HQSTOCK_TRANLIST + code;
		
		if(num > 0) {
			url = url.replace(/num=1/g, 'num=' + num);
		}
		
		mui.ajax({
            type: "get",
			url: url,
			scriptCharset:"GBK",
			dataType:'text',
            timeout: 3000,
            success: function(data) {
            	console.log("success:get_stock_tradeList");
            	console.log(data);
   	
            	cb(data);
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });
	}
	
	
}(mui, window.hq_obj = {}));


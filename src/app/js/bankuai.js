
var bankuaiStockListPage;
function openBankuaiStockListPage(item){
	mui.fire(bankuaiStockListPage, 'display', {data:item});
	//打开
	mui.openWindow({
		id:'bankuaiStockList'
	});
}

(function($$){
	
	var vclassify = new Vue({
		el:'#classify',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){/*重置数据*/
				Object.assign(this.$data,{});
			},
			addItem:function(idx, item){
				this.$set(this.datas, idx, item);
			},
			
			/**
			 * 列表点击事件处理函数：
			 *   根据点击的板块进入详细页面，获取成分股数据 展示
			 * 	 item[3]:行业代码数据
			 **/
			open_detail:function(item){
				
				console.log("open_detail ");
				console.log(item[3]);
				
				openBankuaiStockListPage(item);
			}
		}
	});
	var show_classify_fn = function(dict){
		console.log("show_classify_fn()");
		
		vclassify.resetData();
		
		var i=0;
		var t = [];
		for(var p in dict){			
			t = []
			t.push(dict[p][1]);   /* 0： name*/
			
			var n = parseFloat(dict[p][5]);    /* 1：涨跌点数*/
			n = n.toFixed(2);
			t.push(n);
			
			t.push(dict[p][12]);    /* 2：涨幅*/
			
			t.push(dict[p][0]);    /* 3：行业代码，根据这个代码获取成分股*/
			
			vclassify.addItem(i++, t);
		}
	};
	
	var vmindustry = new Vue({
		el:"#vmindustry",
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){/*重置数据*/
				Object.assign(this.$data,{});
			},
			addItem:function(idx, item){
				this.$set(this.datas, idx, item);
			},
			/**
			 * 列表点击事件处理函数：
			 *   根据点击的板块进入详细页面，获取成分股数据 展示
			 * 	 item[3]:行业代码数据
			 **/
			open_detail:function(item){	
				
				console.log("open_detail ");
				console.log(item[3]);
				
				mui.fire(bankuaiStockListPage,'display',{data:item});
				//打开详情
				mui.openWindow({
					id:'bankuaiStockList'
				});
			}
		}
	});
	
	var show_industy_fn = function(dict){
		console.log("show_industy_fn()");
		
		vmindustry.resetData();
		
		var i=0;
		var t = [];
		for(var p in dict){	
			t = []
			t.push(dict[p][1]);
			
			var n = parseFloat(dict[p][5]);
			n = n.toFixed(2);
			t.push(n);
			
			t.push(dict[p][12]);
			
			t.push(dict[p][0]);    /* 3：行业代码，根据这个代码获取成分股*/
			
			vmindustry.addItem(i++, t);
		}
	};
	
	var vmarea = new Vue({
		el:"#vmarea",
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){/*重置数据*/
				Object.assign(this.$data,{});
			},
			addItem:function(idx, item){
				this.$set(this.datas, idx, item);
			},
			/**
			 * 列表点击事件处理函数：
			 *   根据点击的板块进入详细页面，获取成分股数据 展示
			 * 	 item[3]:行业代码数据
			 **/
			open_detail:function(item){	
				
				console.log("open_detail ");
				console.log(item[3]);
				
				mui.fire(bankuaiStockListPage,'display',{data:item});
				//打开详情
				mui.openWindow({
					id:'bankuaiStockList'
				});
			}
		}
	});
	
	var show_area_fn = function(dict){
		console.log("show_area_fn()");
//		for(var it in dict) {
//			console.log(it);
//			console.log(dict[it]);
//		}
		
		vmarea.resetData();
		
		var i=0;
		var t = [];
		for(var p in dict){	
			t = []
			t.push(dict[p][1]);
			
			var n = parseFloat(dict[p][5]);
			n = n.toFixed(2);
			t.push(n);
			
			t.push(dict[p][12]);
			
			t.push(dict[p][0]);    /* 3：行业代码，根据这个代码获取成分股*/
			
			vmarea.addItem(i++, t);
		}
	};
	
	var vmriselist = new Vue({
		el:"#vmriselist",
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){/**重置数据*/
				Object.assign(this.$data,{});
			},
			setData:function(lstObj){
				tObject.assign(this.$data,lstObj);
			}
		}
	});
	var show_riselist_fn = function(lst){
		console.log("show_riselist_fn()");
		
		vmriselist.datas = lst;
	};
	
	var vmfalllist = new Vue({
		el:"#vmfalllist",
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){/*重置数据*/
				Object.assign(this.$data,{});
			},
			setData:function(lstObj){
				tObject.assign(this.$data,lstObj);
			}
		}
	});
	var show_falllist_fn = function(lst){
		console.log("show_falllist_fn()");
		vmfalllist.datas = lst;
	};
	
	function refreshData(){
		hq_obj.get_FLJK_class(show_classify_fn);
//		
      	hq_obj.get_FLJK_industry(show_industy_fn);
      	
      	hq_obj.get_FLJK_area(show_area_fn);
//    	
      	hq_obj.get_rank_list_data(show_riselist_fn, 0);
//    	
      	hq_obj.get_rank_list_data(show_falllist_fn, 1);
	};
	
//	window.addEventListener('display', function(event){
//		console.log("bankuai.html display event.");
		
	refreshData();   /* 進入加載一次刷新數據*/
//	});
	
})(mui);

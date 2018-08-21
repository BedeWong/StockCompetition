
(function($$){
	$$.init();
	
	var cache_data;
	
	var contest_data = new Vue({
		el:'#contest_data',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			quit_contest: function(data) {
				var  postdata = {}
				postdata.id = data.id;
				app.fillToken(postdata);
				
				mui.ajax({
		            type: "post",
					url: urls.url_quitContest,
					data:postdata,
		            timeout: 3000,
		            success: function(data) {
		            	console.log("success:" + urls.url_quitContest);
		            	
		            	if(data['errcode'] != 0){
		            		plus.nativeUI.toast(data['errmsg']);
		            		return;
		            	}
		            	
		            	plus.nativeUI.toast("退出比賽成功!");
		            	cache_data.join = 2;     // 不可加入
		            	contest_data.datas = cache_data;
		            },
		            error: function(xhr, type, errorThrown) {
		                plus.nativeUI.toast(errorThrown);
		            }
		        });// ajax
			},
			join_contest: function(data){
				var  postdata = {}
				app.fillToken(postdata);
				postdata.contestid = data.id;
				
				mui.ajax({
		            type: "post",
					url: urls.url_joinContest,
					data:postdata,
		            timeout: 3000,
		            success: function(data) {
		            	console.log("success:" + urls.url_joinContest);
		            	
		            	if(data['errcode'] != 0){
		            		plus.nativeUI.toast(data['errmsg']);
		            		return;
		            	}
		            	
		            	plus.nativeUI.toast("加入比賽成功!");
		            	cache_data.join = 1;     // 可退出
		            	contest_data.datas = cache_data;
		            },
		            error: function(xhr, type, errorThrown) {
		                plus.nativeUI.toast(errorThrown);
		            }
		        });// ajax
			},
			enter_market: function(data){
				if(data.join == 0) {
					mui.alert('您还没有加入比赛！','提示','提示',['true'], null, 'div');
					return;
				}else if(data.join == 2) {
					mui.alert('您已經退出該比賽！','提示','提示',['true'], null, 'div');
					return;
				}
				
				var pg_contest_trade = mui.preload({
					url:"contestTrade.html",
					id:"contestTrade",//默认使用当前页面的url作为id
				});
				mui.fire(pg_contest_trade, "display", {data:data});
				mui.openWindow({
					id:'contestTrade'
				});
			}
		}
		
	});
	
	var list_users = new Vue({
		el:'#list-users',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			user_info:function(data){
				var  postdata = {}
				app.fillToken(postdata);
				
				console.log("userinfo：" + data.uid)
				

			}
		}
	});
	
	$$.plusReady(function(){
		console.log("比賽詳情頁面加載完成！");
		
		
	});
	
	function check_in(){
		var postdata = {}
		
		app.fillToken(postdata);
		postdata.id = cache_data.id;
		
		mui.ajax({
            type: "get",
			url: urls.url_checkInContest,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + urls.url_checkInContest);
            	console.log(data['retdata']);
            	
            	if(data['errcode'] != 0){
            		plus.nativeUI.toast(data['errmsg']);
            		return;
            	}
            	
            	cache_data.join = data['retdata'];
            	contest_data.datas = cache_data;
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	function get_rank_list(){
		var postdata = {}
		
		app.fillToken(postdata);
		app.fillRn(postdata);
		postdata.id = cache_data.id;
		
		mui.ajax({
            type: "get",
			url: urls.url_listContestRank,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success:" + urls.url_listContestRank);
//          	console.log(data['retdata']);
            	
            	if(data['errcode'] != 0){
            		plus.nativeUI.toast(data['errmsg']);
            		return;
            	}
            	
            	list_users.datas = data['retdata'];
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	
	window.addEventListener('display', function(event){
		console.log("比賽詳情頁面顯示！");
		console.log(JSON.stringify(event.detail));
		
		cache_data = event.detail.data;
		
		
		$$('.mui-title')[0].innerText = cache_data.title;
		check_in();
		
		get_rank_list();
	});
	
	// 頁面銷毀
	window.addEventListener('refdata', function(event){
		
		contest_data.resetData();
		list_data.resetData();
		
		
		$$('.mui-title')[0].innerText = "";
	});
	
})(mui);

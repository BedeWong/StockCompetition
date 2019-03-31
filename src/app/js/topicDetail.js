(function($$){
	
	/***
	 * 跳轉到 用戶詳細頁面
	 */
	function toUserInfoPage(item) {
		mui.fire(userinfoPage, 'display', {data:item});
		//打开
		mui.openWindow({
			id:'userinfo'
		});
	};
	
	var replysvm = new Vue({
		el:'#reply-items',
		data:{
			datas:{}
		},
		methods:{
			resetData:function(){//重置数据
				Object.assign(this.$data, {});
			},
			toUserinfo:function(item) {
				console.log("点击用户名:" + item.uid + " uname:" + item.uname);
				toUserInfoPage(item);
			},
			upCountReply:function(item) {
				console.log("给評論点赞:" + item.uname);
//				fnUpCountTopic(item);
			}
		}
	});
	
	function fn_ajax(postdata, url, cb){
		
		app.fillToken(postdata);
		
		mui.ajax({
            type: "get",
			url: url,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success: URL:" + url );
            	
            	if(data['errcode'] == 0){
            		cb(data['retdata']);
            	} else {
            		plus.nativeUI.toast(data['errmsg']);
            	}
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
	};
	
	/***8
	 * 获取 文章评论
	 */
	function get_replys(){
		var data = {}
		
		data.aid = pramaData.id;
		data.page = 0;
		data.count = 40;
		
		fn_ajax(data, urls.url_replyListByArticle, function(resp){
			console.log(JSON.stringify(resp));
			
			replysvm.datas = resp;
		});
	};
	
	/*****8
	 * 獲取文章數據
	 */
	function get_topic_dat() {
		var data = {}
		
		data.aid = pramaData.id;
		fn_ajax(data, urls.url_getTopic, function(resp){
			console.log(JSON.stringify(resp));
			
			topicvm.datas = resp;
		});
	}
	
	
	window.addEventListener("display", function(event){			
		pramaData = event.detail.data;
		mui(".mui-title")[0].innerText = pramaData.title;
		
		/***	保存數據到vue對象 **/
		get_topic_dat();
		
		console.log("topic detail page display: " + JSON.stringify(pramaData));
		
		get_replys();
	});
	
	window.addEventListener("refdata", function(event){
		
		console.log("topic detail page refdata: " + JSON.stringify(event.detail.data));
		
		get_replys();
	});
	
	mui.plusReady(function(){
		userinfoPage = mui.preload({
				url:"userinfo.html",
				id:"userinfo",//默认使用当前页面的url作为id
		});
		
		replyPage = mui.preload({
				url:"replay.html",
				id:"replay",//默认使用当前页面的文件名作为id
		});
		
		/******
		 * 處理 收藏、 回復消息  按鈕
		 */
		document.getElementById('btn-mark').addEventListener('tap', function(event){
			console.log("收藏按鈕點擊..");
		});
		
		document.getElementById('btn-reply').addEventListener('tap', function(event){
			console.log("回復按鈕點擊..");
			
			var self = plus.webview.currentWebview();
			datas = pramaData;
			datas.parentView = self;
			mui.fire(replyPage, 'display', {data:datas});
			//打开
			mui.openWindow({
				id:'replay'
			});
		});
	});
	
})(mui);

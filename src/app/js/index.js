
(function($){
	$.init()
	
	mui("#box_1")[0].addEventListener('tap', function(){
		console.log("行情 buttion taped.");
		
		webview = mui.preload({
			id:'market',
			url:'market.html'
		});
		
		//传值给详情页面，通知加载新数据
		mui.fire(webview, 'display',{});
		
		mui.openWindow({
			id:'market'
		});
	});
	
	mui("#box_2")[0].addEventListener('tap', function(){
		console.log("自选  buttion taped.");
		var webview = mui.openWindow({
			url:'myfavoritestock.html',
			extras:{
				name:'testval'  //扩展参数
			}
		});
	});
	
	mui("#box_3")[0].addEventListener('tap', function(){
		console.log("板块  buttion taped.");
		var webview = mui.openWindow({
			url:'bankuai.html',
			extras:{
				name:'testval'  //扩展参数
			}
		});
	});
	
	mui("#box_4")[0].addEventListener('tap', function(){
		console.log("我的持仓  buttion taped.");
		
		var webview = mui.preload({
			id:'mystockposition',
			url:'mystockposition.html'
		});
		
		//传值给详情页面，通知加载新数据
		mui.fire(webview, 'display',{});
		
		mui.openWindow({
			id:"mystockposition"
		});
	});
	
//	mui("#box_5")[0].addEventListener('tap', function(){
//		console.log("大赛  buttion taped.");
//		var curWebView = plus.webview.currentWebview();	
//		var targetWebView = plus.webview.getWebviewById("matchs.html");
//		if (targetWebView == curWebView){ 
//			// 传递 回到顶部 自定义事件（需要 触发 loaded 事件之后 fire 才生效，即页面加载完毕才生效）
//			mui.fire(targetWebView,'backTop',{});
//			return ;
//		}
//		
//		//显示目标选择卡
//		targetWebView.show();
//		//隐藏原选择卡
//		curWebView.hide();
//	});
	mui("#box_6")[0].addEventListener('tap', function(){
		console.log("大牛  buttion taped.");
		var webview = mui.openWindow({
			url:'dalao.html',
			extras:{
				name:'testval'  //扩展参数
			}
		});
	});
	
	var dongtai = new Vue({
    	el:'#dongtai-bar',
    	data:{
    		datas:{}
    	},
    	methods:{
    		
    	}
    });
    
    function get_user_dongtai(){
    	var postdata = {}
    	
    	postdata.userid = app.getState().uid;
	
		app.fillToken(postdata);
	
		mui.ajax({
            type: "get",
			url: urls.url_dongtaiByUser,
			data:postdata,
            timeout: 3000,
            success: function(data) {
            	console.log("success: URL:" + urls.url_dongtaiByUser );
            	
            	if(data['errcode'] == 0){
            		dongtai.datas = data['retdata'];
            		console.log(JSON.stringify(data['retdata']));
            	} else {
            		plus.nativeUI.toast(data['errmsg']);
            	}
            },
            error: function(xhr, type, errorThrown) {
                plus.nativeUI.toast(errorThrown);
            }
        });// ajax
    };
    
    window.addEventListener('display', function(event) {
		console.log("討論頁面顯示。");
	
		get_user_dongtai();
	});
})(mui);

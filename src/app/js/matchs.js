(function($){
	
	mui("#creatematchs")[0].addEventListener('tap', function(){
		console.log("creatematchs buttion taped.");
		var webview = mui.openWindow({
			url:'createMatch.html',
			extras:{
				name:'create'  //扩展参数
			}
		});
	});
	
	mui("#searchmatchs")[0].addEventListener('tap', function(){
		console.log("searchmatchs buttion taped.");
		var webview = mui.openWindow({
			url:'searchMatchs.html',
			extras:{
				name:'create'  //扩展参数
			}
		});
	});
})(mui);

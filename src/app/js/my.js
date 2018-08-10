
(function($){
	$.init()
	
	// tabwidget 切換
	mui("#tabwealth")[0].addEventListener('tap', function(){
		console.log("wealth");
		
		document.getElementById("tabwealth").classList.add("curtab");
		document.getElementById("tabchart").classList.remove("curtab");
		
		document.getElementById("wealthchart").classList.remove("mui-hidden");
		document.getElementById("trendchart").classList.add("mui-hidden");
	});
	mui("#tabchart")[0].addEventListener('tap', function(){
		console.log("chart");
		
		document.getElementById("tabchart").classList.add("curtab");
		document.getElementById("tabwealth").classList.remove("curtab");
		
		document.getElementById("trendchart").classList.remove("mui-hidden");
		document.getElementById("wealthchart").classList.add("mui-hidden");
	});
	
	mui("#setting")[0].addEventListener('tap', function(){
		console.log("setting buttion taped.");
		var webview = mui.openWindow({
			url:'setting.html',
			extras:{
				name:'setting'  //扩展参数
			}
		});
	});
	
	
	
	
	
})(mui);

(function($){
	$.init()
	
	// tabwidget 切換
	
	mui("#tab1")[0].addEventListener('tap', function(){
		console.log("tab1");
		
		document.getElementById("tab1").classList.add("curtab");
		document.getElementById("tab2").classList.remove("curtab");
		document.getElementById("tab3").classList.remove("curtab");
		document.getElementById("tab4").classList.remove("curtab");
		
		document.getElementById("hot").classList.remove("mui-hidden");
		document.getElementById("newest").classList.add("mui-hidden");
		document.getElementById("care").classList.add("mui-hidden");
		document.getElementById("mine").classList.add("mui-hidden");
	});
	mui("#tab2")[0].addEventListener('tap', function(){
		console.log("tab2");
		
		document.getElementById("tab2").classList.add("curtab");
		document.getElementById("tab1").classList.remove("curtab");
		document.getElementById("tab3").classList.remove("curtab");
		document.getElementById("tab4").classList.remove("curtab");
		
		document.getElementById("newest").classList.remove("mui-hidden");
		document.getElementById("hot").classList.add("mui-hidden");
		document.getElementById("care").classList.add("mui-hidden");
		document.getElementById("mine").classList.add("mui-hidden");
	});
	mui("#tab3")[0].addEventListener('tap', function(){
		console.log("tab3");
		
		document.getElementById("tab3").classList.add("curtab");
		document.getElementById("tab2").classList.remove("curtab");
		document.getElementById("tab1").classList.remove("curtab");
		document.getElementById("tab4").classList.remove("curtab");
		
		document.getElementById("care").classList.remove("mui-hidden");
		document.getElementById("newest").classList.add("mui-hidden");
		document.getElementById("hot").classList.add("mui-hidden");
		document.getElementById("mine").classList.add("mui-hidden");
	});
	mui("#tab4")[0].addEventListener('tap', function(){
		console.log("tab4");
		
		document.getElementById("tab4").classList.add("curtab");
		document.getElementById("tab2").classList.remove("curtab");
		document.getElementById("tab3").classList.remove("curtab");
		document.getElementById("tab1").classList.remove("curtab");
		
		document.getElementById("mine").classList.remove("mui-hidden");
		document.getElementById("newest").classList.add("mui-hidden");
		document.getElementById("care").classList.add("mui-hidden");
		document.getElementById("hot").classList.add("mui-hidden");
	});
	
	
	
	
})(mui);

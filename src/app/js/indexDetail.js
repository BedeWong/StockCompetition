(function($$){
	console.log("indexDetail.js");
	
	var img_baseurl = 'http://image.sinajs.cn/newchart/';
	
	mui("#container-4").on('tap', ".tab-chart", function(ev){
		var id = this.getAttribute("id");
		var targetdiv = NaN;
		
		console.log(id);
		
		switch(id){
			case "tab-min":
				targetdiv = $("#chart-min");
				
				var imgurl = img_baseurl+"min/n/" + detailData.code + '.gif';
				mui("#img-min")[0].setAttribute('src', imgurl);
				
				break;
			case "tab-day":
				targetdiv = $("#chart-day");
				
				var imgurl = img_baseurl+"daily/n/" + detailData.code + '.gif';
				console.log(imgurl);
				mui("#img-day")[0].setAttribute('src', imgurl);
				break;
			case "tab-week":
				targetdiv = $("#chart-week");
				mui("#img-week")[0].setAttribute('src', img_baseurl+"weekly/n/" + detailData.code + '.gif');
				break;
			case "tab-month":
				targetdiv = $("#chart-month");
				mui("#img-month")[0].setAttribute('src', img_baseurl+"monthly/n/" + detailData.code + '.gif');
				break;
		}
		
		if (targetdiv == NaN) return;
		
		targetdiv.removeClass("mui-hidden").siblings().addClass("mui-hidden");
		$(this).addClass("tab-chart-cur").siblings().removeClass('tab-chart-cur');   // 當前點擊tab標簽
	});

		
})(mui);

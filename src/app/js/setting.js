
(function($){
	$.init();
	
	$.plusReady(function() {
		var LoginPage = plus.webview.getWebviewById("main");
		var login_loaded_flag = false;
		if(!LoginPage){
			LoginPage = $.preload({
				"id": 'main',
				"url": 'main.html'
			});
		}else{
			login_loaded_flag = true;
		}
		
		LoginPage.addEventListener("loaded",function () {
			main_loaded_flag = true;
		});
		
		var toLogin = function() {
			if (login_loaded_flag == true){
				$.fire(LoginPage, 'show', null);
				LoginPage.show("pop-in");
			}
		};
		
		var exitButton = document.getElementById('exit');
		// 点击退出
		exitButton.addEventListener('tap', function(event) {
			app.exit();
			toLogin();
		});
	});/**plusReady*/
	
})(mui);

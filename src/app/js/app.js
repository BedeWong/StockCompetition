
//baseurl = 'http://192.168.43.188:8001';
//baseurl = 'http://192.168.191.4:8001';
baseurl = 'http://120.79.208.53:8001';

window.urls = {
	url_picCode : baseurl+'/piccode',
	url_getSMSCode : baseurl+'/api/checkpic',
	
	url_login : baseurl + '/api/login',
	url_getUserinfo : baseurl + '/api/getuserinfo',
	
	url_addStock2Favorite :baseurl + '/api/favoritestock/add',
	url_getFavoriteStock : baseurl + '/api/favoritestock/list',
	url_delFromFavoriteStock : baseurl + '/api/favoritestock/del',
	url_checkStockInFavorite : baseurl + '/api/favoritestock/checkin',
	
	// 獲取持有的股票信息
	url_getMyStocks : baseurl + "/api/holdstocks/list",
	
	// 股票交易相關
	url_buystock : baseurl + "/api/stocks/buy",
	url_salestock : baseurl + "/api/stocks/sale",
	url_getTradeHistory: baseurl + "/api/stocks/history/tradelist",
	url_invokeStock : baseurl + "/api/stocks/invoke",
	
	// 比賽相關
	url_createContest : baseurl + '/api/contest/create',
	url_joinContest : baseurl + '/api/contest/join',
	url_quitContest : baseurl + '/api/contest/quit',
	url_listContest : baseurl + '/api/contest/list',
	url_listUserContest : baseurl + '/api/contest/list/user',
	url_checkInContest : baseurl + '/api/contest/checkin',
	url_listContestRank : baseurl + '/api/contest/detail/ranklist',
	
	// 比賽持倉：
	url_listContestUserStocks : baseurl + "/api/contest/stocks/list",
	url_contestUserInfo : baseurl + "/api/contest/userinfo",
	
	url_contestStockBuy : baseurl + "/api/contest/stocks/buy",
	url_contestStockSale : baseurl + "/api/contest/stocks/sale",
	url_contestStockInvoke : baseurl + "/api/contest/stocks/invoke",
	url_contestHistoryList : baseurl + "/api/contest/stocks/history/tradelist",
	
	// 討論處理接口
	url_airticlePublish : baseurl + '/api/article/add',
	url_topichot : baseurl + '/api/article/hot',						// 获取 热门， 最新、 我的关注、与我相关的动态
	url_topiccare : baseurl + '/api/dongtai/list/user',
	url_topicnewest : baseurl + '/api/article/newest',
	url_topicmine : baseurl + '/api/article/list/uid',
	url_topiccheckupcount : baseurl + "/api/article/upcount/check",
	url_topicUpcount : baseurl + '/api/article/upcount',
	url_getTopic : baseurl + '/api/article/id',
	
	url_replyDel : baseurl + '/api/reply/del',
	url_replyAdd : baseurl + "/api/reply/add",
	url_replyUpcount : baseurl + '/api/reply/upcount',
	url_replyCheckUpcount : baseurl + '/api/reply/upcount/check',
	url_replyAddReply : baseurl + '/api/reply/addreply',
	url_replyNewest : baseurl + '/api/reply/newest',
	url_replyListByArticle : baseurl + '/api/article/reply/list',
	
	// 動態
	url_dongtaiByUid : baseurl + '/api/dongtai/list/uid',
	url_dongtaiByUser : baseurl + '/api/dongtai/list/user',
	
	// 粉絲關係
	url_followerAdd : baseurl + '/api/follower/add',     // 關注
	url_followerDel : baseurl + '/api/follower/del',
	url_followerCount : baseurl + '/api/follower/count',
	url_followerCheck : baseurl + '/api/follower/check',
	
};

/**
 * 演示程序当前的 “注册/登录” 等操作，是基于 “本地存储” 完成的
 * 当您要参考这个演示程序进行相关 app 的开发时，
 * 请注意将相关方法调整成 “基于服务端Service” 的实现。
 **/
(function($, owner) {
	/**
	 * 用户登录
	 **/
	owner.login = function(loginInfo, callback) {
		callback = callback || $.noop;
		loginInfo = loginInfo || {};
		loginInfo.loginId = loginInfo.loginId || '';
		loginInfo.password = loginInfo.password || '';
		if (loginInfo.loginId.length < 2) {
			return callback('账号不正确');
		}
		if (loginInfo.password.length < 6) {
			return callback('密码最短为 6 个字符');
		}
//		var users = JSON.parse(localStorage.getItem('$users') || '[]');
//		var authed = users.some(function(user) {
//			return loginInfo.loginId == user.account && loginInfo.password == user.password;
//		});
		
		console.log("ajax...");
		console.log($.param(loginInfo));
		var authed = false;
		$.ajax(urls.url_login, {
			data : $.param(loginInfo),
			type : 'POST',
			timeout : 5000,
			crossDomain: true,
	        xhrFields: {
	            withCredentials: true
	        },
			success : function(dat) {
				console.log(dat.errcode);
				console.log(dat.token);
				console.log(dat.retdata);
				if(dat.errcode == 0) {
					$.toast("登录成功!");
					authed = true;
				}//成功返回
				else {
					authed = false;
				}
				
				if (authed) {
					return owner.createState(dat, callback);
				} else {
					return callback('用户名或密码错误');
				}
			},//end success
			error: function(code, type, msg) {  
                $.alert("error:" + code + "\ntype = " + type + "\nmsg:" + msg);  
           		authed = false;
			}
		});
	};
	
	owner.getUserInfo = function(cb) {
		cb = cb || $.noop;
		var state = owner.getState();
		
		udata = {
			uname : state.uname,
			utoken : state.token
		};
		
		var authed = false;
		$.ajax(urls.url_getUserinfo, {
			data : $.param(udata),
			type : 'POST',
			timeout : 5000,
			crossDomain: true,
	        xhrFields: {
	            withCredentials: true
	        },
			success : function(dat) {
				console.log(dat.errcode);
				console.log(dat.token);
				console.log(dat.retdata);
				if(dat.errcode == 0) {
					$.toast("登录成功!");
					authed = true;
				}//成功返回
				else {
					authed = false;
				}
				
				if (authed) {
					owner.createState(dat, $.noop);
					return cb(authed);
				}
			},//end success
			error: function(code, type, msg) {  
                $.alert("error:" + code + "\ntype = " + type + "\nmsg:" + msg);  
           		authed = false;
           		return cb(authed);
			}
		});
	};

	owner.createState = function(resp, callback) {
		var state = owner.getState();
		state.token = resp.token;
		
		/*用戶信息*/
		userinfo = resp.retdata;
		state.uid = userinfo.uid;
		state.uname = userinfo.uname;
		state.uaddress = userinfo.uaddress;
		state.umobile = userinfo.umobile;
		state.usex = userinfo.usex;
		state.uvisitors = userinfo.uvisitors;
		state.uheadurl = userinfo.uheadurl;
		state.udescibe = userinfo.udescibe;
		state.udescimg = userinfo.udescimg;
		state.ulevel = userinfo.ulevel;
		state.utype = userinfo.utype;
		state.uearnrate = userinfo.uearnrate;
		state.uearnratemon = userinfo.uearnratemon;
		state.uwinrate = userinfo.uwinrate;
		state.umoney = userinfo.umoney;
		state.ulastlogin = userinfo.ulastlogin;
		state.uemail = userinfo.uemail;
		state.urank = userinfo.urank;
		
		owner.setState(state);
		return callback();
	};

	/**
	 * 新用户注册
	 **/
	owner.reg = function(regInfo, callback) {
		callback = callback || $.noop;
		regInfo = regInfo || {};
		regInfo.account = regInfo.account || '';
		regInfo.password = regInfo.password || '';
		if (regInfo.account.length < 5) {
			return callback('用户名最短需要 5 个字符');
		}
		if (regInfo.password.length < 6) {
			return callback('密码最短需要 6 个字符');
		}
		if (!checkEmail(regInfo.email)) {
			return callback('邮箱地址不合法');
		}
		var users = JSON.parse(localStorage.getItem('$users') || '[]');
		users.push(regInfo);
		localStorage.setItem('$users', JSON.stringify(users));
		return callback();
	};

	/**
	 * 获取当前状态
	 **/
	owner.getState = function() {
		var stateText = localStorage.getItem('$state') || "{}";
		return JSON.parse(stateText);
	};

	/**
	 * 设置当前状态
	 **/
	owner.setState = function(state) {
		state = state || {};
		localStorage.setItem('$state', JSON.stringify(state));
		//var settings = owner.getSettings();
		//settings.gestures = '';
		//owner.setSettings(settings);
	};
	
	/***
	 *  填充token
	 * @param {Object} data
	 */
	owner.fillToken = function(data) {
		if(typeof(data) != 'object'){
			console.log("fillToken err");
		}
		
		var state = owner.getState()
		
		data.utoken = state.token;
		data.uid = state.uid;
	};
	
	/***
	 * 填充隨機值，强制服務器刷新數據
	 * @param {Object} data
	 */
	owner.fillRn = function(data){
		data.rn =  (new Date()).getTime() / 1000; 
	};

	var checkEmail = function(email) {
		email = email || '';
		return (email.length > 3 && email.indexOf('@') > -1);
	};

	/**
	 * 找回密码
	 **/
	owner.forgetPassword = function(email, callback) {
		callback = callback || $.noop;
		if (!checkEmail(email)) {
			return callback('邮箱地址不合法');
		}
		return callback(null, '新的随机密码已经发送到您的邮箱，请查收邮件。');
	};

	/**
	 * 获取应用本地配置
	 **/
	owner.setSettings = function(settings) {
		settings = settings || {};
		localStorage.setItem('$settings', JSON.stringify(settings));
	}

	/**
	 * 设置应用本地配置
	 **/
	owner.getSettings = function() {
			var settingsText = localStorage.getItem('$settings') || "{}";
			return JSON.parse(settingsText);
		}
		/**
		 * 获取本地是否安装客户端
		 **/
	owner.isInstalled = function(id) {
		if (id === 'qihoo' && mui.os.plus) {
			return true;
		}
		if (mui.os.android) {
			var main = plus.android.runtimeMainActivity();
			var packageManager = main.getPackageManager();
			var PackageManager = plus.android.importClass(packageManager)
			var packageName = {
				"qq": "com.tencent.mobileqq",
				"weixin": "com.tencent.mm",
				"sinaweibo": "com.sina.weibo"
			}
			try {
				return packageManager.getPackageInfo(packageName[id], PackageManager.GET_ACTIVITIES);
			} catch (e) {}
		} else {
			switch (id) {
				case "qq":
					var TencentOAuth = plus.ios.import("TencentOAuth");
					return TencentOAuth.iphoneQQInstalled();
				case "weixin":
					var WXApi = plus.ios.import("WXApi");
					return WXApi.isWXAppInstalled()
				case "sinaweibo":
					var SinaAPI = plus.ios.import("WeiboSDK");
					return SinaAPI.isWeiboAppInstalled()
				default:
					break;
			}
		}
	}
	
	$.plusReady(function() {
		var settingPage = $.preload({
			"id": 'setting',
			"url": 'setting.html'
		});
		
		var self = plus.webview.currentWebview();
		console.log(self.id);
		if(self.id != "main") {
			console.log(self.id + " , " + self.getTitle() + "  return.");
			return ;
		}
		
		//--  雙擊返回退出
		$.oldBack = mui.back;
		var backButtonPress = 0;
		$.back = function(event) {
			backButtonPress++;
			if (backButtonPress > 1) {
				plus.runtime.quit();
			} else {
				plus.nativeUI.toast('再按一次退出应用');
			}
			setTimeout(function() {
				backButtonPress = 0;
			}, 1000);
			return false;
		};
		
		// 配置頁面
		var subpages = ['index.html','contest.html', 'discuss.html', 'my.html'];
      	var subpage_style = {
		    top: '0px',  
		    bottom: '51px'  
		}; 

		//  底部tab切換
  		for (var i = 0; i < subpages.length; i++){
  			var sub = plus.webview.create(
  				subpages[i],
  				subpages[i],
  				subpage_style
  			);
  			if (i >0){	//隐藏其他页面
  				sub.hide(); 
  			}
  			self.append(sub); //加入子页面
  		}
  		
  		//选择卡切换
  		var changeTab = function(e,targetTab){
  			var curTab = document.getElementsByClassName('mui-active')[0].getAttribute('href');
  			var curWebView = plus.webview.getWebviewById(curTab);
      		var targetWebView = plus.webview.getWebviewById(targetTab);
      		if (targetWebView == curWebView){ 
      			// 传递 回到顶部 自定义事件（需要 触发 loaded 事件之后 fire 才生效，即页面加载完毕才生效）
      			mui.fire(targetWebView,'backTop',{});
      			console.log("未點擊新頁面。");
      			return ;
      		}
      		
      		//显示目标选择卡
      		targetWebView.show();
      		
      		//發送display事件
      		mui.fire(targetWebView,'display',{});
      		
      		//隐藏原选择卡
      		curWebView.hide();
  		};
  		// 监听选择卡点击事件
      	mui('.mui-bar-tab').on('tap','a',function(e){
      		// 获取目标选择卡id
      		var targetTab = this.getAttribute('href');
      		
      		console.log(targetTab);
      		
      		var state = owner.getState();
      		if(state) {
      			console.log(state.uname);
      			console.log(state.uid);
      		}
      		// 切换选择卡
      		changeTab(this,targetTab);
      	});
	});  // end plusReady
}(mui, window.app = {}));


// 获取cookie方法
function getCookie(name) {
	console.log(document.cookie)
	console.log(sessionStorage.getItem(name))
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
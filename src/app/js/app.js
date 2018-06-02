
baseurl = 'http://10.254.248.15:8001';

urls = {
	url_picCode : baseurl+'/piccode',
	url_getSMSCode : baseurl+'/api/checkpic',
	url_login : baseurl + '/api/login'
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
		console.log(JSON.stringify(loginInfo));
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
				console.log(dat.errmsg);
				console.log(dat.token);
				if(dat.errcode == 0) {
					$.toast("登录成功!");
					authed = true;
				}//成功返回
				else {
					authed = false;
				}
				
				if (authed) {
					return owner.createState(loginInfo, dat.token, callback);
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

	owner.createState = function(info, token, callback) {
		var state = owner.getState();
		state.account = info.loginId;
		state.token = token;
		state.pwd   = info.password;
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
}(mui, window.app = {}));


// 获取cookie方法
function getCookie(name) {
	console.log(document.cookie)
	console.log(sessionStorage.getItem(name))
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
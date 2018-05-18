#### sina 行情接口：
**接口获取说明：**
> 接口根据网址```http://finance.sina.com.cn/realstock/company/sh603036/nc.shtml```获取到js文件依次查找调用的接口，不保证接口一直能用。  
本页数据获取来源js文件：  
```http://n.sinaimg.cn/finance/66ceb6d9/20180116/stock20180116.js?cn=1.0```


##### 个股最新通知
```
http://vip.stock.finance.sina.com.cn/api/jsonp.php/var%20noticeData=/CB_AllService.getMemordlistbysymbol?num=8&PaperCode=603036
```
##### 个股内外盘口
```
https://hq.sinajs.cn/etag.php?_=1526480603456&list=sh603036
```

##### 个股分时成交
> 时间，成交价，成交量
```
http://vip.stock.finance.sina.com.cn/quotes_service/view/vML_DataList.php?asc=j&symbol=sh603036&num=11
```

##### 个股新闻
```
http://news.sinajs.cn/rn=1526480727250&maxcnt=20&scnt=20&list=sh603036,gg_sh603036,ntc_sh603036,blog_sh603036,tg_sh603036,lcs_sh603036
```

##### 个股大单
> 时间  价格 量 性质（s/b）
```
http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_BillList.php?sort=ticktime&symbol=sh603036&num=11
```

##### 个股逐笔数据
> 时间 价格 量 性质（S/B）  
trade_INVOL_OUTVOL: 内盘, 外盘  （手数/100)
```
http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=11&symbol=sh603036
```

##### 实时行情
```
http://hq.sinajs.cn/rn=1526482881989&list=s_sh000001,s_sz399001,CFF_RE_IC0,rt_hkHSI,gb_$dji,gb_ixic,b_SX5E,b_UKX,b_NKY,hf_CL,hf_GC,hf_SI,hf_CAD 
```

##### 个股所属板块（有误）
```
http://hq.sinajs.cn/rn=1526482882575&list=sh603036,sh603036_i,bk_new_qtxy
```

##### 个股资金流入
> 散单  小单 大单  特大单  
流入额， 流通盘比例， 占换手比例
```
http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/var%20moneyFlowData=/MoneyFlow.ssi_ssfx_flzjtj?daima=sh603036
```

##### 个股公告
```
http://vip.stock.finance.sina.com.cn/api/jsonp.php/var%20noticeData=/CB_AllService.getMemordlistbysymbol?num=8&PaperCode=601333
```

#####
> 暂时不详
``` 
http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price_list.php?&symbol=sh601333&num=11
```

##### 
> 个股停牌时间（有误）
```
http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/var%20continueTime=/CN_StockForGDTXService.getStockStatus04Info?code=sh600283
```
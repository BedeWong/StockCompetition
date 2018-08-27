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
http://news.sinajs.cn/rn=1526480727250&maxcnt=20&scnt=20&list=sh603036\ngg_sh603036\nntc_sh603036\nblog_sh603036\ntg_sh603036\nlcs_sh603036
```

##### 个股大单
> 时间  价格 量 性质（s/b）
```
http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_BillList.php?sort=ticktime&symbol=sh603036&num=11
```

##### 个股逐笔数据
> 时间 价格 量 性质（S/B）  
trade_INVOL_OUTVOL: 内盘\n 外盘  （手数/100)
```
http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=11&symbol=sh603036
```

##### 实时行情
```
http://hq.sinajs.cn/rn=1526482881989&list=s_sh000001\ns_sz399001\nCFF_RE_IC0\nrt_hkHSI\ngb_$dji\ngb_ixic\nb_SX5E\nb_UKX\nb_NKY\nhf_CL\nhf_GC\nhf_SI\nhf_CAD 
```

##### 个股所属板块（有误）
```
http://hq.sinajs.cn/rn=1526482882575&list=sh603036\nsh603036_i\nbk_new_qtxy
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

##### 板块
> 获取板块数据
```
http://money.finance.sina.com.cn/q/view/newFLJK.php?param=class
class : 概念
industry ： 行业
area ： 地域
json:
{
    "gn_bdgn": "gn_bdgn\n百度概念\n15\n15.846\n-0.36466666666667\n-2.2495476229643\n112190318\n1196066805\nsh601127\n0.875\n17.300\n0.150\n小康股份"\n
    "gn_xmgn": "gn_xmgn\n小米概念\n39\n16.690263157895\n-0.24\n-1.4175798554442\n314490703\n4758379192\nsz300408\n1.073\n24.480\n0.260\n三环集团"
}
{
    "hangye_ZA01": "hangye_ZA01\n农业\n15\n7.6826666666667\n-0.14666666666667\n-1.8732970027248\n77233207\n521416013\n\n0\n\n\n"\n
    "hangye_ZA03": "hangye_ZA03\n林业\n5\n11.284\n-0.214\n-1.8611932510002\n5953240\n46976921\n\n0\n\n\n"
}
```
##### 获取个股涨幅数据列表
> 这个接口获取涨幅排名的股数， 根据这个接口的返回值 使用 hq.sina.com 获取行情数据
```
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=changepercent&asc=0&node=hs_a
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=changepercent&asc=1&node=hs_a
```

##### 獲取板塊、概念、指數成分股數量
```
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hs_a
```
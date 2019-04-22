#coding=utf-8

from handlers import user_info
from handlers import verify_code
from handlers import favorite_stocks
from handlers import user_hold_stocks
from handlers import trade
from handlers import contest
from handlers import contest_trade
from handlers import article
from handlers import reply
from handlers import user_follower
from handlers import dongtai

urls = [
    (r'/api/login', user_info.LoginHandler),
    (r'/api/logout', user_info.LogoutHandler),
    (r'/api/register', user_info.RegisterHanler),
    (r'/api/getuserinfo', user_info.GetUserInfo),
    (r'/api/user/([0-9]+)', user_info.UserInfo),

    (r'/api/piccode', verify_code.PicCodeHandler),  # 图片验证码生成
    (r'/api/checkpic', verify_code.SMSCodeHandler),  # 验证码验证，发送短信

    # 用戶自選股
    (r'/api/favoritestock/add', favorite_stocks.AddStock2FavoriteHandler),
    (r'/api/favoritestock/del', favorite_stocks.DelStockHandler),
    (r'/api/favoritestock/checkin', favorite_stocks.CheckStockHandler),
    (r'/api/favoritestock/list', favorite_stocks.GetStockListHandler),

    # 持倉股票
    (r'/api/holdstocks/list', user_hold_stocks.GetStockList),

    # 股票交易記錄相關
    (r'/api/stocks/buy', trade.BuyStockHander),  # 股票委托买
    (r'/api/stocks/sale', trade.SaleStockHandler),  # 股票委托卖
    (r'/api/stocks/revoke', trade.RevokeStockHandler),  # 股票委托撤单
    (r'/api/stocks/orders', trade.ListOrder),  # 委托单列表
    (r'/api/stocks/history/tradelist', trade.GetTradeHistoryHandler),  # 成交记录

    # 比賽相關
    (r'/api/contest/create', contest.ContestCreate),
    (r'/api/contest/join', contest.ContestJoin),
    (r'/api/contest/list', contest.Contest_get_list),
    (r'/api/contest/list/user', contest.Contest_get_user_contest),
    (r'/api/contest/quit', contest.ContestQuit),
    (r'/api/contest/detail/ranklist', contest.Contest_get_contest_rank),
    (r'/api/contest/checkin', contest.Contest_check_in_contest),
    (r'/api/contest/userinfo', contest.ContestUserInfo),

    (r'/api/contest/stocks/list', contest_trade.ListUserContestStocks),  # 用户该场比赛的持股
    (r'/api/contest/stocks/buy', contest_trade.BuyStockHander),  # 比赛中委托买单
    (r'/api/contest/stocks/sale', contest_trade.SaleStockHandler),
    (r'/api/contest/stocks/revoke', contest_trade.RevokeStockHandler),
    (r'/api/contest/stocks/orders', trade.ListOrder),  # 委托单列表
    (r'/api/contest/stocks/history/tradelist', contest_trade.GetTradeHistoryHandler),

    # 話題 評論
    (r'/api/article/add', article.addArticle),
    (r'/api/article/del', article.delArticle),
    (r'/api/article/upcount/check', article.checkUpcount),
    (r'/api/article/id', article.getArticleById),
    (r'/api/article/list/uid', article.getArtilceByUid),
    (r'/api/article/hot', article.getHotArticle),
    (r'/api/article/newest', article.getNewestArticle),
    (r'/api/article/upcount', article.UpcountArticle),
    (r'/api/article/upcount-only', article.UpcountArticleOnly),

    (r'/api/reply/add', reply.addReply),
    (r'/api/reply/del', reply.delReply),
    (r'/api/reply/upcount', reply.upcountReply),
    (r'/api/reply/upcount/check', reply.checkUpcount),
    (r'/api/reply/addreply', reply.addReplyReply),
    (r'/api/reply/newest', reply.getNewestReply),
    (r'/api/article/reply/list', reply.getArticleReplys),

    # 動態
    (r'/api/dongtai/list/uid', dongtai.GetDongTaiByUid),
    (r'/api/dongtai/list/user', dongtai.getDongTaiByUser),

    #follower 粉絲關係
    (r'/api/follower/add', user_follower.FollowerRelationAdd),
    (r'/api/follower/del', user_follower.FollowerRelationDel),
    (r'/api/follower/count', user_follower.GetFollowersCount),
    (r'/api/follower/check', user_follower.CheckUserFollowerRelation),
]

def main():
    pass


if __name__ == '__main__':
    main()
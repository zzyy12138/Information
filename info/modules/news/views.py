"""create by zhouzhiyang"""

from info import db
from info.models import User, News
from info.utils.commons import user_login_data
from info.utils.response_code import RET
from . import news_blu
from flask import render_template, session, current_app, g, jsonify, abort, request


# 新闻详情展示
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blu.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
    # 根据新闻编号,获取新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询新闻失败")

    # 判断新闻对象是否存在,(以后实现,统一处理404页面)
    if not news:
        abort(404)

    # 查询热门新闻数据
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(8).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # 将新闻对象列表,转成字典列表
    click_news_list = []
    for item in news_list:
        click_news_list.append(item.to_dict())

    # 判断用户对当前新闻是否有收藏
    is_collected = False
    # 用户登陆,并且新闻在用户的收藏列表, 那么证明用户收藏了该新闻
    if g.user and news in g.user.collection_news:
        is_collected = True

    data = {
        "user_info": g.user.to_dict() if g.user else "",
        "click_news_list": click_news_list,
        "news": news.to_dict(),
        "is_collected": is_collected
    }

    return render_template('news/detail.html', data=data)

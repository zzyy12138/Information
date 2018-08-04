"""create by zhouzhiyang"""
from flask import request

from info import redis_store
from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blu
from flask import render_template, current_app, session, jsonify


# 功能描述:首页新闻列表展示
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据
@index_blu.route('/newslist')
def news_list():
    """
    思路分析:
    1.获取参数
    2.校验参数,参数类型转换
    3.分页查询,用到paginate
    4.获取到分页对象属性,总页数,当前页,当前页对象
    5.将新闻对象列表,转成字典列表
    6.返回响应,携带数据
    :return:
    """
    # 1.获取参数
    cid = request.args.get('cid')
    page = request.args.get('page', 1)  # 获取不到默认值是1
    per_page = request.args.get('per_page', 10)  # 获取不到默认值是10

    # 2.校验参数,参数类型转换
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        per_page = 10

    # 3.分页查询,用到paginate
    try:
        # 判断分类编号是否不等于1
        filters = []
        if cid != "1":
            filters.append(News.category_id == cid)

        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # 4.获取到分页对象属性,总页数,当前页,当前页对象
    totalPages = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5.将新闻对象列表,转成字典列表
    newsList = []
    for news in items:
        newsList.append(news.to_dict())

    # 6.返回响应,携带数据
    return jsonify(errno=RET.OK, errmsg="查询成功", newsList=newsList, totalPage=totalPages, currentPage=currentPage)


# 首页内容
@index_blu.route('/', methods=['GET', 'POST'])
def show_index_page():
    # 测试redis
    redis_store.set('name', 'zhangsan')

    # 测试session
    # session['name'] = 'banzhang'
    # print('helloworld')

    # logging.debug('调试信息')
    # logging.info('详细信息!!')
    # logging.warning('警告信息')
    # logging.error('错误信息')

    # 上面四句话可以写成如下形式,使用current_app,多了分割线,但是在文件中输出的内容完全一样
    # current_app.logger.debug('调试信息++')
    # current_app.logger.info('详细信息!!++')
    # current_app.logger.warning('警告信息++')
    # current_app.logger.error('错误信息++')

    # 获取session中的用户信息
    user_id = session.get("user_id")

    # 获取用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 查询热门新闻前10条
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="新闻查询失败")

    # 将新闻对象列表,转成字典列表
    click_news_list = []
    for news in news_list:
        click_news_list.append(news.to_dict())

    # 查询分类数据
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="分类查询失败")

    # 将分类对象列表,转成字典列表
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    data = {
        # 判断user如果有值,返回左边内容,否则返回右边的值
        "user_info": user.to_dict() if user else "",
        "click_news_list": click_news_list,
        "categories": category_list
    }

    return render_template('news/index.html', data=data)


# 浏览器在访问,在访问每个网站的时候,都会发送一个Get请求,向/favicon.ico地址获取logo
# app中提供了方法send_static_file,会自动寻找static静态文件下面的资源
@index_blu.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')

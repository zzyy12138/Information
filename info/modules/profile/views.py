"""create by zhouzhiyang"""
from flask import render_template, g, request, jsonify, current_app

from info import constants, db
from info.models import News, Category
from info.utils.commons import user_login_data
from info.utils.response_code import RET
from . import profile_blu
# from hjutils.image_storage import image_storage
from info.utils.image_storage import image_storage


# 获取收藏列表
# 请求路径: /user/collection
# 请求方式:GET
# 请求参数:p(页数)
# 返回值: user_collection.html页面
@profile_blu.route('/collection')
@user_login_data
def news_collection():
    """
    思路分析:
    1.获取参数,获取默认第一页
    2.参数类型转换,字符串转整数,因为paginate中使用的是整数
    3.分页查询
    4.获取到分页对象中的属性,总页数,当前页,当前页对象
    5.对象列表,转成字典列表
    6.拼接数据,渲染页面
    :return:
    """
    # 1.获取参数,获取默认第一页
    page = request.args.get('p', 1)

    # 2.参数类型转换,字符串转整数,因为paginate中使用的是整数
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 3.分页查询
    try:
        # 获取第page页, 每页有10条, 不进行错误输出
        paginate = g.user.collection_news.order_by(News.create_time.desc()).paginate(page, 10, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # 4.获取到分页对象中的属性,总页数,当前页,当前页对象
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5.对象列表,转成字典列表
    news_list = []
    for item in items:
        news_list.append(item.to_dict())

    # 6.拼接数据,渲染页面
    data = {
        "totalPage": totalPage,
        "currentPage": currentPage,
        "news_list": news_list
    }
    return render_template('news/user_collection.html', data=data)


# 密码修改
# 请求路径: /user/pass_info
# 请求方式:GET,POST
# 请求参数:GET无, POST有参数,old_password, new_password
# 返回值:GET请求: user_pass_info.html页面,data字典数据, POST请求: errno, errmsg
@profile_blu.route('/pass_info', methods=['GET', 'POST'])
@user_login_data
def pass_info():
    """
    思路分析:
    1.第一次进来GET,渲染页面
    2.获取参数
    3.校验参数
    4.判断旧密码是否正确
    5.设置新密码
    6.返回响应
    :return:
    """
    # 1.第一次进来GET,渲染页面
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')

    # 2.获取参数
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    # 3.校验参数
    if not all([old_password, new_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 4.判断旧密码是否正确
    if not g.user.check_passowrd(old_password):
        return jsonify(errno=RET.DATAERR, errmsg="旧密码错误")

    # 5.设置新密码
    g.user.password = new_password

    # 6.返回响应
    return jsonify(errno=RET.OK, errmsg="修改成功")


# 头像设置
# 请求路径: /user/pic_info
# 请求方式:GET,POST
# 请求参数:无, POST有参数,avatar
# 返回值:GET请求: user_pci_info.html页面,data字典数据, POST请求: errno, errmsg,avatar_url
@profile_blu.route('/pic_info', methods=['GET', 'POST'])
@user_login_data
def pic_info():
    """
    思路分析:
    1.第一次进来GEt请求,直接返回页面,携带用户数据
    2.获取参数
    3.校验参数
    4.上传头像
    5.判断头像是否上传成功
    6.设置用户头像属性
    7.返回响应携带头像
    :return:
    """
    # 1.第一次进来GEt请求,直接返回页面,携带用户数据
    if request.method == 'GET':
        data = {
            "user_info": g.user.to_dict() if g.user else ""
        }
        return render_template('news/user_pic_info.html', data=data)

    # 2.获取参数
    avatar = request.files.get('avatar')

    # 3.校验参数
    if not avatar:
        return jsonify(errno=RET.PARAMERR, errmsg="图像不能为空")

    # 4.上传头像
    try:
        image_name = image_storage(avatar.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="七牛云上传异常")

    # 5.判断头像是否上传成功
    if not image_name:
        return jsonify(errno=RET.NODATA, errmsg="图片上传失败")

    # 6.设置用户头像属性
    g.user.avatar_url = image_name;

    # 7.返回响应携带头像
    data = {
        "avatar_url": constants.QINIU_DOMIN_PREFIX + image_name
    }
    return jsonify(errno=RET.OK, errmsg="上传成功", data=data)


# 展示用户基本信息
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@profile_blu.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():
    """
    思路分析:
    1.如果第一次进入是GET请求,携带用户数据渲染页面
    2.获取参数
    3.校验参数
    4.设置用户信息
    5.返回响应
    :return:
    """
    # 1.如果第一次进入是GET请求,携带用户数据渲染页面
    if request.method == "GET":
        data = {
            "user_info": g.user.to_dict() if g.user else ""
        }
        return render_template('news/user_base_info.html', data=data)

    # 2.获取参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 3.校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    if not gender in ["MAN", "WOMAN"]:
        return jsonify(errno=RET.DATAERR, errmsg="性别异常")

    # 4.设置用户信息
    g.user.nick_name = nick_name
    g.user.signature = signature
    g.user.gender = gender

    # 5.返回响应
    return jsonify(errno=RET.OK, errmsg="修改成功")


# 展示个人中心
@profile_blu.route('/show_user_info')
@user_login_data
def show_user_info():
    data = {
        "user_info": g.user.to_dict() if g.user else ""
    }

    return render_template('news/user.html', data=data)

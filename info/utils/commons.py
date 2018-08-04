# 用来存储功能的内容


# 自定义过滤器,实现热门新闻颜色提示
from flask import session, current_app, g
from functools import wraps


def do_index_class(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    else:
        return ""


# 登陆装饰器
def user_login_data(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        # 获取用户编号
        user_id = session.get('user_id')

        # 查询用户对象
        user = None
        if user_id:
            try:
                from info.models import User
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        # 保存用户对象到g
        g.user = user

        return view_func(*args, **kwargs)

    return wrapper

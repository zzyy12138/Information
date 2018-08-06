"""create by zhouzhiyang"""
from flask import render_template, g
from info.utils.commons import user_login_data
from . import profile_blu


# 展示个人中心
@profile_blu.route('/show_user_info')
@user_login_data
def show_user_info():
    data = {
        "user_info": g.user.to_dict() if g.user else ""
    }

    return render_template('news/user.html', data=data)

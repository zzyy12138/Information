"""create by zhouzhiyang"""
from flask import Blueprint

#创建用户蓝图对象
profile_blu = Blueprint("profile",__name__,url_prefix='/user')

from . import views
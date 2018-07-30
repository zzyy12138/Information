"""create by zhouzhiyang"""
from flask import Blueprint

# 创建首页蓝图对象
index_blu = Blueprint("index", __name__)

# 使用蓝图装饰视图函数
from . import views

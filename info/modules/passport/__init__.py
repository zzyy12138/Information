from flask import Blueprint

#创建认证蓝图
passport_blu = Blueprint("passport",__name__,url_prefix='/passport')

from . import views
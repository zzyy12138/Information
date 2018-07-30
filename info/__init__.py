"""create by zhouzhiyang"""
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config_dict


# 工厂方法
def create_app(config_name):
    # 创建app
    app = Flask(__name__)

    config = config_dict.get(config_name)

    # 加载配置类到app
    app.config.from_object(config)

    # 创建SQLAlchemy对象,关联app
    db = SQLAlchemy(app)

    # 创建redis对象
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 初始化session
    Session(app)

    # 设置csrf保护
    CSRFProtect(app)

    return app

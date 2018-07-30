"""create by zhouzhiyang"""
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

"""
配置信息:
1.数据库配置
2.redis配置
3.session配置: 主要是用来保存用户登陆信息(登陆的时候再来看)
4.csrf配置: 当修改服务器资源的时候保护(post,put,delete,dispatch)
5.日志文件: 记录程序运行的过程,如果使用print来记录,控制台没有保存数据,线上上线print不需要打印了.
6.迁移配置
"""


# 设置基础配置类
class Config(object):
    # 设置启动模式,秘钥
    DEBUG = True
    SECRET_KEY = "jfkdjfkdk"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/Information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 设置session配置信息
    SESSION_TYPE = 'redis'  # 保存类型
    SESSION_USE_SIGNER = True  # 签名存储
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 2  # 设置存储时间为2天,单位秒


# 加载配置类到app
app.config.from_object(Config)

# 创建SQLAlchemy对象,关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 初始化session
Session(app)

# 设置csrf保护
CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run()

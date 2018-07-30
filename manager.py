"""create by zhouzhiyang"""
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config

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

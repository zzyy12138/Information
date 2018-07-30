"""create by zhouzhiyang"""

# 设置基础配置类
import logging
import redis


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


# 开发环境配置信息
class DevelopConfig(Config):
    pass


# 生产环境配置信息(线上)
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR


# 测试环境配置信息
class TestingConfig(Config):
    TESTING = True


# 通过字典统一访问配置类
config_dict = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "testing": TestingConfig,
}

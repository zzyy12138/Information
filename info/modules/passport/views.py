import random

from flask import make_response, request, jsonify, current_app, json, session

from info import redis_store, constants, db
# from info.libs.yuntongxun.sms import CCP
# from info.models import User
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu
import re


# 功能描述: 图片验证码
# 请求地址: /passport/image_code
# 请求方式: GET
# 请求参数: 随机字符串(uuid)
# 返回值:  返回图片
@passport_blu.route('/image_code')
def get_image_code():
    """
    思路分析:
    1.获取参数
    2.校验参数
    3.生成图片验证码
    4.保存到redis
    5.返回
    :return:
    """

    # 1.获取参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    # 2.校验参数
    if not cur_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    # 3.生成图片验证码
    try:
        name, text, image_data = captcha.generate_captcha()

        # 4.保存到redis
        # 参数1:保存到redis的key
        # 参数2:图片验证码
        # 参数3:过期时间
        redis_store.set('image_code:%s' % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        # 判断有没有上个编号
        if pre_id:
            redis_store.delete('image_code:%s' % pre_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="验证操作失败")

    # 5.返回图片验证码
    response = make_response(image_data)
    response.headers["Content-Type"] = 'image/jpg'
    return response

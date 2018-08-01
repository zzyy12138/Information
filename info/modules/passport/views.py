from flask import make_response

from info.utils.captcha.captcha import captcha
from . import passport_blu

#功能描述: 图片验证码
#请求地址: /passport/image_code
#请求方式: GET
#请求参数: 随机字符串(uuid)
#返回值:  返回图片
@passport_blu.route('/image_code')
def get_image_code():

    #1.生成图片验证码
    name,text,image_data = captcha.generate_captcha()

    #2.返回图片验证码
    response = make_response(image_data)
    response.headers["Content-Type"] = 'image/jpg'
    return response

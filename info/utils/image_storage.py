# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'Y3GQWzWc-P8lDWyikez1kmMHSFRFD25nrcA7isCX'
secret_key = 'r5QCceIfRxP-UIUlK_u_MQnDDSxUC1_CU8S-caRC'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = 'information'

# 上传到七牛后保存的文件名,如果编写按照自己的,如果不写七牛云维护图片名称
# key = 'my-python-logo.png'

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, None, 3600)


def image_storage(image_data):
    # 要上传文件的本地路径
    # localfile = './11.jpg'
    # ret, info = put_file(token, None, localfile)
    ret, info = put_data(token, None, image_data)

    # 上传成功,返回图片名称,失败返回空
    if info.status_code == 200:
        return ret.get("key")
    else:
        return ""


if __name__ == '__main__':
    file = open('./11.jpg', 'rb')
    print(image_storage(file.read()))
    file.close()

from flask import Blueprint, request
from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/signup")
@bp.route('/signup_info', methods=['POST'])
def signup_info():
    user_type = request.forms.get('user_type', "user")
    phone = request.forms.get('phone', "")
    password = request.forms.get('password', "")
    nid = request.forms.get('nid', "")
    user_name = request.forms.get('user_name', "")
    user_dic = {}
    user_dic['user_type'] = user_type
    user_dic['phone'] = phone
    user_dic['password'] = password
    user_dic['nid'] = nid
    user_dic['user_name'] = user_name
    try:
        flag = signup_user(user_dic) # TODO:
        if flag：
            return {"code":True,"message":"注册成功"}
        else:
            return {"code":False,"message":"注册失败"}
    except Exception:
        return {"status": "error"}
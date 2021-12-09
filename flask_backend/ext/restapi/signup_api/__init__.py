from flask import Blueprint, request
from flask_backend.ext.database import *
from flask_backend.ext.restapi.user_api.models import User

bp = Blueprint("signup_api", __name__, url_prefix="/api/signup")


@bp.route('/signup_info', methods=['POST'])
def signup_info():
    signup_data = request.get_json()
    user_type = signup_data["user_type"]
    phone = signup_data["phone"]
    password = signup_data["password"]
    nid = signup_data["nid"]
    user_name = signup_data["user_name"]
    user_dic = {}
    user_dic['user_type'] = user_type
    user_dic['phone'] = phone
    user_dic['password'] = password
    user_dic['nid'] = nid
    user_dic['user_name'] = user_name
    try:
        flag = signup_user(user_dic)
        if flag:
            return {"code":True,"message":"注册成功"}
        else:
            return {"code":False,"message":"注册失败"}
    except Exception:
        return {"status": "error"}


def init_app(app):
    app.register_blueprint(bp)
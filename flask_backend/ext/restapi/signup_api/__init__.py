from flask import Blueprint, request
from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/signup")
@bp.route('/signup_info', methods=['POST'])
def signup_info():
    user_type = request.form.get('user_type', "user")
    phone = request.form.get('phone', "")
    password = request.form.get('password', "")
    nid = request.form.get('nid', "")
    user_name = request.form.get('user_name', "")
    user_dic = {}
    user_dic['user_type'] = user_type
    user_dic['phone'] = phone
    user_dic['password'] = password
    user_dic['nid'] = nid
    user_dic['user_name'] = user_name
    try:
        flag = signup_user(user_dic.to_bson()) # TODO:
        return flag
    except Exception:
        return {"status": "error"}
from flask import Blueprint, request
from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/login")


@bp.route('/login_info', methods=['GET'])
def login_info():
    phone = request.args.get('phone', "")
    input_password = request.args.get('password', "")
    try:
        true_password = get_password_by_phone(phone)  # TODO:
        if true_password == -1:
            return {"code": -1, "message": "用户不存在"}
        else:
            if true_password != input_password:
                return {"code": -2, "message": "密码错误"}
            else:
                return {"code": 1, "message": "验证通过"}
    except Exception:
        return {"status": "error"}

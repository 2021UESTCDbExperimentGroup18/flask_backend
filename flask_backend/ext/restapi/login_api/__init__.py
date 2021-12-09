from flask import Blueprint, request

from flask_backend.ext.database import *

bp = Blueprint("login_api", __name__, url_prefix="/api/login")


@bp.route('/login_info', methods=['GET', "POST"])
def login_info():
    data = request.get_json()
    phone = data['phone']
    input_password = data['password']
    try:
        true_password = get_password_by_phone(phone)
        if true_password is None:
            return {"code": -1, "message": "用户不存在"}
        else:
            if true_password != input_password:
                return {"code": -2, "message": "密码错误"}
            else:
                user_id = get_user_id_by_phone(phone)
                return {"code": 1, "message": "验证通过", "user": {
                    "phone": phone,
                    "user_id": user_id
                }}
    except Exception as e:
        return {"code": -3, "message": e}


def init_app(app):
    app.register_blueprint(bp)

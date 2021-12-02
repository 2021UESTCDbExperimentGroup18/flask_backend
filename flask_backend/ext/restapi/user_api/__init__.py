from flask import Blueprint, request
from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/users")


@bp.route('/user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id', "")
    result = get_user_by_user_id(user_id)
    user = User(**result)
    return user.to_json()


@bp.route('/user_list', methods=['GET'])
def get_user_list():
    user_type = request.args.get('user_type', "user")
    page_id = int(request.args.get('page_id', 1))

    try:
        pass
    except Exception:
        return {"status": "error"}


def init_app(app):
    app.register_blueprint(bp)

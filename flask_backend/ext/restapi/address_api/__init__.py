from flask import Blueprint, request

bp = Blueprint('address', __name__, url_prefix="/api")


@bp.route("get_address")
def get_address():
    data = request.get_json()
    user_id = data["user_id"]
    address_list = get_address_by_user_id(user_id)

    if address_list:
        return {"code": 1, "address_list": address_list}
    else:
        return {"code": 1, "address_list": []}


def init_app(app):
    app.register_blueprint(bp)
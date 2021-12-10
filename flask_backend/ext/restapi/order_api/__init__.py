import json
import logging

from flask import Blueprint, request

from flask_backend.ext.database import *

bp = Blueprint("order_api", __name__, url_prefix="/api/orders")


@bp.route('/getOrder', methods=["POST"])
def get_user_order():
    data = request.get_json()
    user_id = data["user_id"]

    user_order = get_order_by_user(user_id)

    if user_order:
        return {"code": 1, "orders": user_order}
    else:
        return {"code": -1, "orders": []}


@bp.route('/addOrder', methods=['POST'])
def add_orders():
    data = request.get_json()
    user_id = data["user_id"]
    order_id = ""
    try:
        for product in data["products"]:
            order_id = add_order(user_id, product, order_id)
            if not order_id:
                return {"code": -1, "message": "添加订单异常"}
        delete_shopping_cart_by_user(user_id)
        return {"code": 1, "message": "购买成功"}
    except Exception as e:
        logging.error(e)
        return {"code": -1, "message": "添加订单异常"}


def init_app(app):
    app.register_blueprint(bp)

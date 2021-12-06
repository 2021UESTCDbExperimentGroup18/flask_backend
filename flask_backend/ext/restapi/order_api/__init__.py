from flask import Blueprint, request
from flask_backend.ext.database import *
import json

bp = Blueprint("order_api", __name__, url_prefix="/api/orders")


@bp.route('/order_num', methods=['GET'])
def order_num():
    user_id = request.args.get('user_id', "")
    order_status = request.args.get('order_status', "")
    try:
        order_num = get_order_num(user_id,order_status)  # TODO:
        return order_num
    except Exception:
        return {"status": "error"}


@bp.route('/valid_order', methods=['GET'])
def valid_order():
    page_id = int(request.args.get('page_id', 1))
    try:
        validorder_list = get_valid_order(page_id)  # TODO:
        order_object_list = []
        for order in validorder_list:
            orderid = order['_id']
            del order['id']
            order['order_id'] = orderid
            order_object = Order(**order)
            order_object_list.append(order_object.to_json())
        return order_object_list
    except Exception:
        return {"status": "error"}


@bp.route('/order_search', methods=['GET'])
def order_search():
    page_id = int(request.args.get('page_id', 1))
    user_id = request.args.get('user_id', "")
    user_type = request.args.get('user_type', "")
    try:
        all_order_list = get_all_order_list(user_type,page_id,user_id)  # TODO:
        order_object_list = []
        for order in all_order_list:
            orderid = order['_id']
            del order['id']
            order['order_id'] = orderid
            order_object = Order(**order)
            order_object_list.append(order_object.to_json())
        return order_object_list
    except Exception:
        return {"status": "error"}

@bp.route('/order_details', methods=['GET'])
def order_details():
    order_id = request.args.get('order_id', "")
    try:
        order_info = get_prder_by_id(order_id)   # TODO:
        orderid = order_info['_id']
        del order_info['id']
        order_info['order_id'] = orderid
        order_object = Order(**order_info)
        return order_object.to_json()
    except Exception:
        return {"status": "error"}

@bp.route('/new_order', methods=['POST'])
def new_order():
    postform = json.loads(request.get_data(as_text = True)) # TODO:
    order = Order()
    order.order_status = "active"
    order.user_id = postform["user_id"]
    commodities_list = []
    for commodity in postform["commodities"]:
        commodity_mes = Commodity()
        commodity_mes.commodity_id = commodity[0]
        commodity_mes.commodity_number = int(Commodity[1])
        commodities_list.append(commodity_mes)
    order.commodities = commodities_list
    order.address_id = postform["address_id"]
    try:
        flag = new_order(order.to_bson())
        if flag：
            return {"code":True,"message":"添加成功"}
        else:
            return {"code":False,"message":"添加失败"}
    except Exception:
        return {"status": "error"}
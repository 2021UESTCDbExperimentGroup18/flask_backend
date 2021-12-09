from flask import Blueprint, request

from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/users")


@bp.route('/user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id', "")
    try:
        result = get_user_by_user_id(user_id)  # TODO:
        userid = result['_id']
        # del result['_id']
        result['user_id'] = str(userid)
        result['user_name'] = user_id
        user = User(**result)
        return user.to_json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@bp.route('/add_address', methods=['POST'])
def add_address():
    user_id = request.forms.get('user_id', "")
    phone = request.forms.get('phone', "")
    address = request.forms.get('address', "")
    address_info = {}
    address_info['user_id'] = user_id
    address_info['phone'] = phone
    address_info['address'] = address
    try:
        flag = add_address_to_db(address_info)  # TODO: 函数名待定
        if flag:
            return {"code": True, "message": "添加成功"}
        else:
            return {"code": False, "message": "添加失败"}
    except Exception:
        return {"status": "error"}


@bp.route('/remove_address', methods=['POST'])
def remove_address():
    address_id = request.forms.get('address_id', "")
    try:
        flag = remove_address_from_db(address_id)  # TODO:
        if flag:
            return {"code": True, "message": "移除成功"}
        else:
            return {"code": False, "message": "移除失败"}
    except Exception:
        return {"status": "error"}


@bp.route('/check_password', methods=['POST'])
def check_password():
    user_id = request.forms.get('user_id', "")
    input_password = request.forms.get('password', "")
    try:
        true_password = get_password_by_id(user_id)  # TODO:
        if true_password == -1:
            return {"code": -1, "message": "用户不存在"}
        else:
            if true_password != input_password:
                return {"code": -2, "message": "密码错误"}
            else:
                return {"code": 1, "message": "验证通过"}
    except Exception:
        return {"status": "error"}


@bp.route('/change_password', methods=['POST'])
def change_password():
    user_id = request.forms.get('user_id', "")
    new_password = request.forms.get('password', "")
    try:
        flag = change_password(user_id, new_password)
        if flag:
            return {"code": True, "message": "修改成功"}
        else:
            return {"code": False, "message": "修改失败"}
    except Exception:
        return {"status": "error"}


@bp.route('/search', methods=['GET'])
def search():  # 获取用户地址列表
    user_id = request.args.get('user_id', "")
    try:
        address_list = get_address_list(user_id)  # TODO:
        address_object_list = []
        for addr_dic in address_list:
            addr_id = addr_dic['_id']
            del addr_dic['_id']
            addr_dic['address_id'] = addr_id
            address_object = Address(**addr_dic)
            address_object_list.append(address_object.to_json())
        return user_object_list
    except Exception:
        return {"status": "error"}


@bp.route('/user_list', methods=['GET'])
def get_user_list():
    user_type = request.args.get('user_type', "user")
    page_id = int(request.args.get('page_id', 1))
    try:
        user_info_list = get_user_by_page(user_type, page_id)  # TODO:函数名待更改
        user_object_list = []
        for user_dic in user_info_list:
            userid = user_dic['_id']
            user_dic['user_id'] = str(userid)
            user_object = User(**user_dic)
            user_object_list.append(user_object.to_json())
        return {"users": user_object_list}
    except Exception as e:
        return {"status": "error", "message": e}


@bp.route('/shoppingCart/getShoppingCart', methods=['POST'])
def get_shopping_cart():
    data = request.get_json()
    user_id = data['user_id']
    shopping_data = get_shopping_cart_by_user_id(user_id)
    if shopping_data is None:
        return {"code": -1, "shoppingCartData": []}
    else:
        return {"code": 1, "shoppingCartData": shopping_data}


@bp.route('/shoppingCart/addShoppingCart', methods=['POST'])
def add_shopping_cart():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']

    item = get_cart_item_by_user_product(user_id, product_id)
    code = 1
    if item is not None:
        code = 2

    flag = add_to_shopping_cart(user_id, product_id)
    shopping_cart_data = get_shopping_cart_by_user_id(user_id)

    if flag and shopping_cart_data is not None:
        return {"code": code, "message": "添加购物车成功", "shoppingCartData": shopping_cart_data}
    else:
        return {"code": -1, "message": "添加购物车失败", "shoppingCartData": shopping_cart_data}


@bp.route('/shoppingCart/updateShoppingCart', methods=['POST'])
def update_user_shopping_cart():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']
    num = data['num']

    id = update_shopping_cart(user_id, product_id, num)

    if id:
        return {"code": 1, "message": "修改购物车成功"}
    else:
        return {"code": -1, "message": "修改购物车失败"}


@bp.route('/shoppingCart/deleteShoppingCart', methods=['POST'])
def delete_user_shopping_item():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']

    id = delete_shopping_cart(user_id, product_id)

    if id:
        return {"code": 1, "message": "修改购物车成功"}
    else:
        return {"code": -1, "message": "修改购物车失败"}


def init_app(app):
    app.register_blueprint(bp)

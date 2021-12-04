from flask import Blueprint, request
from flask_backend.ext.database import *

bp = Blueprint("user_api", __name__, url_prefix="/api/users")


@bp.route('/user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id', "")
    try:
        result = get_user_by_user_id(user_id)  # TODO:
        userid = result['_id']
        del result['_id']
        result['user_id'] = userid
        user = User(**result)
        return user.to_json()
    except Exception:
        return {"status": "error"}    
    

@bp.route('/add_address', methods=['POST'])
def add_address():
    user_id = request.args.get('user_id', "")
    phone = request.args.get('phone', "")
    address = request.args.get('address', "")
    address_info = {}
    address_info['user_id'] = user_id
    address_info['phone'] = phone
    address_info['address'] = address
    try:
        flag = add_address_to_db(address_info.to_bson())  # TODO: 函数名待定
        return flag
    except Exception:
        return {"status": "error"} 

@bp.route('/remove_address', methods=['POST'])
def remove_address():
    address_id = request.args.get('address_id', "")
    try:
        flag = remove_address_from_db(address_id)   # TODO: 
        return flag
    except Exception:
        return {"status": "error"} 

@bp.route('/check_password', methods=['POST'])
def check_password():
    user_id = request.args.get('user_id', "")
    input_password = request.args.get('password', "")
    try:
        true_password = get_password_by_id(user_id)  # TODO:
        if true_password == -1:
            return -1
        else:
            if true_password != input_password:
                return -2
            else:
                return 1  
    except Exception:
        return {"status": "error"}

@bp.route('/change_password', methods=['POST'])
def change_password():
    user_id = request.args.get('user_id', "")
    new_password = request.args.get('password', "")
    try:
        flag = change_password(user_id,new_password)
        return flag
    except Exception:
        return {"status": "error"}


@bp.route('/search', methods=['GET'])
def search():   #获取用户地址列表
    user_id = request.args.get('user_id', "")
    try:
        address_list = get_address_list(user_id)  # TODO:
        address_object_list = []
        for addr_dic in address_list:
            addr_id = addr_dic['_id']
            del addr_dic['_id']
            addr_dic['address_id'] = addr_id
            address_object = Address(**addr_dic)
            address_object_list.append(address_object)
        return user_object_list.to_json()
    except Exception:
        return {"status": "error"}   


@bp.route('/user_list', methods=['GET'])
def get_user_list():
    user_type = request.args.get('user_type', "user")
    page_id = int(request.args.get('page_id', 1))
    try:
        user_info_list = get_user_list(user_type, page_id)   # TODO:函数名待更改
        user_object_list = []
        for user_dic in user_info_list:
            userid = user_dic['_id']
            del user_dic['_id']
            user_dic['user_id'] = userid
            user_object = User(**user_dic)
            user_object_list.append(user_object)
        return user_object_list.to_json()
    except Exception:
        return {"status": "error"}   




def init_app(app):
    app.register_blueprint(bp)



bp2 = Blueprint("user_api", __name__, url_prefix="/api/login")
@bp2.route('/login_info', methods=['GET'])
def login_info():
    phone = request.args.get('phone', "")
    input_password = request.args.get('password', "")
    try:
        true_password = get_password_by_phone(phone)  # TODO:
        if true_password == -1:
            return -1
        else:
            if true_password != input_password:
                return -2
            else:
                return 1  
    except Exception:
        return {"status": "error"}

bp3 = Blueprint("user_api", __name__, url_prefix="/api/signup")
@bp2.route('/signup_info', methods=['GET'])
def signup_info():
    user_type = request.args.get('user_type', "user")
    phone = request.args.get('phone', "")
    password = request.args.get('password', "")
    nid = request.args.get('nid', "")
    user_name = request.args.get('user_name', "")
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



from flask_backend.utils.base_model import BaseMethod
from pydantic import BaseModel, constr
from datetime import datetime


class User(BaseModel, BaseMethod):
    user_id: str
    user_name: str
    user_type: constr(regex=r'^(user|rider|admin)$')
    password: constr(min_length=6, max_length=100)
    phone: constr(regex=r'^1[3456789]\d{9}$')
    nid: constr(min_length=18, max_length=18)
    create_time: datetime
    modify_time: datetime


class Address(BaseModel, BaseMethod):
    address_id:str
    user_id: str
    address: str
    phone: constr(regex=r'^1[3456789]\d{9}$')


class ShoppingCartItem(BaseModel, BaseMethod):
    user_id: str
    check: bool
    num: int
    price: float
    productID: str
    productImg: str
    productName: str

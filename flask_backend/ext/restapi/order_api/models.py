from flask_backend.utils.base_model import BaseMethod
from pydantic import BaseModel, constr
from datetime import datetime


class Commodity(BaseModel, BaseMethod):
    commodity_id: str
    # commodity_description: str  # TODO:  picture or description
    commodity_number: str


class Order(BaseModel, BaseMethod):
    order_id: str
    order_status: constr(regex=r'^(active|done|unassigned|cancelled)$')
    user_id: str
    rider_id: str
    product_id: str
    product_picture: str
    product_num: int
    address_id: str
    product_price: float
    create_time: datetime
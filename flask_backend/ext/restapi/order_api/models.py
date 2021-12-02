from flask_backend.utils.base_model import BaseMethod
from pydantic import BaseModel, constr
from datetime import datetime


class Order(BaseModel, BaseMethod):
    order_id: str
    order_status: constr(regex=r'^(active|done|unassigned|cancelled)$')
    user_id: str
    rider_id: str
    commodities: str
    address_id: str
    create_time: datetime

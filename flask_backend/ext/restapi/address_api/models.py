from pydantic import BaseModel, constr
from flask_backend.utils.base_model import BaseMethod


class Address(BaseModel, BaseMethod):
    user_id: str
    address: str
    phone: constr(regex=r'^1[3456789]\d{9}$')

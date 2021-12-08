from flask_backend.utils.base_model import BaseMethod
from pydantic import BaseModel


class Product(BaseModel, BaseMethod):
    product_intro: str
    product_name: str
    product_price: float
    product_selling_price: float

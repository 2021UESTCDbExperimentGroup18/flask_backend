from flask_backend.utils.base_model import BaseMethod
from pydantic import BaseModel


class Commodity(BaseModel, BaseMethod):
    commodity_id: str
    commodity_description: str
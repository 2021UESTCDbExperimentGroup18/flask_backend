from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import Field

from flask_backend.utils.objectid import PydanticObjectId


class BaseMethod:
    id: Optional[PydanticObjectId] = Field(None, alias="_id")

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data

import bson
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_backend.ext.restapi.user_api.models import User


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_user_by_user_id(user_id):
    try:

        pipeline = [
            {
                "$match": {
                    "user_id": user_id
                }
            }
        ]

        user = db.user.aggregate(pipeline).next()
        return user

    except StopIteration as _:
        return None
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return {}



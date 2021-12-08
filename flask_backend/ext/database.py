import bson
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import gridfs
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_backend.ext.restapi.user_api.models import User
import logging


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


def get_password_by_phone(phone):
    try:

        pipeline = [
            {
                "$match": {
                    "phone": phone
                }
            }
        ]

        user = db.user.aggregate(pipeline).next()
        return user.password

    except StopIteration as _:
        return None
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return {}


def get_product_by_page(page_size, page):
    try:

        pipeline = [
            {
                "$match": {}
            },
            {
                "$limit": page_size
            },
            {
                "$skip": page_size * (page - 1)
            }
        ]

        products = [product for product in db.good.aggregate(pipeline)]
        return products

    except StopIteration as _:
        return None
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return []


def get_product_by_name(name, page_size, page):
    try:

        pipeline = [
            {
                "$match": {
                    "product_name": {
                        "$regex": name
                    }
                }
            },
            {
                "$limit": page_size
            },
            {
                "$skip": page_size * (page - 1)
            }
        ]

        products = [product for product in db.good.aggregate(pipeline)]
        return products

    except StopIteration as _:
        return None
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return []


def get_product_by_id(product_id):
    try:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(product_id)
                }
            },
        ]
        products = [product for product in db.good.aggregate(pipeline)]
        return products
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return []


def get_user_by_page(user_type, page_id):
    try:
        pipeline = [
            {
                "$match": {
                    "user_type": user_type
                }
            },
           {
               "$limit": 10
           },
           {
               "$skip": 10 * (page_id - 1)
           }
        ]
        users = [user for user in db.user.aggregate(pipeline)]
        return users
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return []


def get_pic_by_product_id(product_id):
    picture_id = db.good.find_one({
        "_id": ObjectId(product_id)
    }, {"_id": 0, "picture_id": 1})["picture_id"]
    grid_fs = gridfs.GridFS(db)
    return grid_fs.get(ObjectId(picture_id))


def upload_image(image, name):
    grid_fs = gridfs.GridFS(db)
    return grid_fs.put(image, content_type=image.content_type, filename=name)


def get_product_name_total(name):
    try:
        return db.good.count_documents({"product_name": {
            "$regex": name
        }})
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return 0


def get_product_total():
    try:
        return db.good.count_documents({})
    except Exception as e:
        print(e)  # TODO: 重构日志系统，将此处修改为对应日志记录
        return 0

import codecs
import datetime
import logging

import gridfs
from bson.objectid import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

from flask_backend.ext.restapi.user_api.models import ShoppingCartItem


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

        pipeline = [{"$match": {"user_id": user_id}}]

        user = db.user.aggregate(pipeline).next()
        return user

    except StopIteration as _:
        return None
    except Exception as e:
        logging.error(e)
        return {}


def get_product_by_page(page_size, page):
    try:

        pipeline = [{"$match": {}}, {"$limit": page_size}, {"$skip": page_size * (page - 1)}]

        products = [product for product in db.good.aggregate(pipeline)]
        return products

    except StopIteration as _:
        return None
    except Exception as e:
        logging.error(e)
        return []


def get_product_by_name(name, page_size, page):
    try:

        pipeline = [
            {"$match": {"product_name": {"$regex": name}}},
            {"$limit": page_size},
            {"$skip": page_size * (page - 1)},
        ]

        products = [product for product in db.good.aggregate(pipeline)]
        return products

    except StopIteration as _:
        return None
    except Exception as e:
        logging.error(e)
        return []


def get_product_by_id(product_id):
    try:
        pipeline = [
            {"$match": {"_id": ObjectId(product_id)}},
        ]
        products = [product for product in db.good.aggregate(pipeline)]
        return products
    except Exception as e:
        logging.error(e)
        return []


def get_user_by_page(user_type, page_id):
    try:
        pipeline = [{"$match": {"user_type": user_type}}, {"$limit": 10}, {"$skip": 10 * (page_id - 1)}]
        users = [user for user in db.user.aggregate(pipeline)]
        return users
    except Exception as e:
        logging.error(e)
        return []


def get_pic_by_product_id(product_id):
    picture_id = db.good.find_one({"_id": ObjectId(product_id)}, {"_id": 0, "picture_id": 1})["picture_id"]
    grid_fs = gridfs.GridFS(db)
    image = grid_fs.get(ObjectId(picture_id))
    base64_data = codecs.encode(image.read(), "base64")
    image = base64_data.decode("utf-8")
    return image


def upload_image(image, name):
    grid_fs = gridfs.GridFS(db)
    return grid_fs.put(image, content_type=image.content_type, filename=name)


def get_product_name_total(name):
    try:
        return db.good.count_documents({"product_name": {"$regex": name}})
    except Exception as e:
        logging.error(e)
        return 0


def get_product_total():
    try:
        return db.good.count_documents({})
    except Exception as e:
        logging.error(e)
        return 0


def get_password_by_phone(phone):
    try:
        password = db.user.find_one({"phone": phone}, {"_id": 0, "password": 1})["password"]
        if len(password) == 0:
            return None
        return password
    except Exception as e:
        logging.error(e)
        return None


def get_user_id_by_phone(phone):
    try:
        id = db.user.find_one({"phone": phone}, {"_id": 1})["_id"]
        return str(id)
    except Exception as e:
        logging.error(e)
        return None


def get_shopping_cart_by_user_id(user_id):
    try:
        pipeline = [
            {"$match": {"user_id": user_id}},
        ]

        shopping_cart = [item for item in db.shopping_cart.aggregate(pipeline)]
        result = []
        for i in range(len(shopping_cart)):
            item = ShoppingCartItem(**shopping_cart[i]).to_json()
            item["id"] = str(shopping_cart[i]["_id"])
            item["max_num"] = 9999
            result.append(item)

        return result

    except StopIteration as _:
        return None
    except Exception as e:
        logging.error(e)
        return None


def get_cart_item_by_user_product(user_id, product_id):
    try:
        item = db.shopping_cart.find_one({"user_id": user_id, "productID": product_id})
        if item is None:
            return None
        cart_item = ShoppingCartItem(**item).to_json()
        cart_item["id"] = str(item["_id"])
        cart_item["max_num"] = 9999
        return cart_item
    except Exception as e:
        logging.error(e)
        return None


def add_to_shopping_cart(user_id, product_id):
    item = get_cart_item_by_user_product(user_id, product_id)
    if item is not None:
        return update_shopping_cart(user_id, product_id, item["num"] + 1)
    product = get_product_by_id(product_id)[0]
    document = {
        "user_id": user_id,
        "check": False,
        "num": 1,
        "price": float(product["product_selling_price"]),
        "productID": product_id,
        "productImg": get_pic_by_product_id(product_id),
        "productName": product["product_name"],
    }
    try:
        id = db.shopping_cart.insert_one(document)
        return id
    except Exception as e:
        logging.error(e)
        return None


def update_shopping_cart(user_id, product_id, num):
    item = get_cart_item_by_user_product(user_id, product_id)
    if item is None:
        return False

    id = db.shopping_cart.update_one({"user_id": user_id, "productID": product_id}, {"$set": {"num": num}})
    return id


def delete_shopping_cart(user_id, product_id):
    id = db.shopping_cart.delete_one({"user_id": user_id, "productID": product_id})
    return id


def get_order_by_user(user_id):
    try:
        pipeline = [
            {"$match": {"user_id": user_id}},
        ]

        shopping_cart = [item for item in db.order.aggregate(pipeline)]
        result = []
        for i in range(len(shopping_cart)):
            item = ShoppingCartItem(**shopping_cart[i]).to_json()
            item["id"] = str(shopping_cart[i]["_id"])
            item["max_num"] = 9999
            result.append(item)

        return result

    except StopIteration as _:
        return None
    except Exception as e:
        logging.error(e)
        return None
    return []


def signup_user(user_dict):
    user_dict["create_time"] = datetime.datetime.now()
    user_dict["modify_time"] = datetime.datetime.now()
    try:
        id = db.user.insert_one(user_dict)
        return id
    except Exception as e:
        logging.error(e)
        return False

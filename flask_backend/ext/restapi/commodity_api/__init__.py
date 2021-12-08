from crypt import methods

from flask import Blueprint, request
from flask_backend.ext.database import *
from flask_backend.ext.restapi.commodity_api.models import *

bp = Blueprint("product_api", __name__, url_prefix="/api/product")


@bp.route("/getAllProduct", methods=["GET"])
def get_all_product():
    page = int(request.args.get("currentPage", "1"))
    page_size = int(request.args.get("pageSize", "16"))
    try:
        products = get_product_by_page(page_size, page)
        product_json = [Product(**x).to_json() for x in products]
        for i in range(len(products)):
            product_json[i]["product_id"] = str(products[i]["_id"])
        total_product = get_product_total()
        return {"Product": product_json, "total": total_product}
    except Exception as e:
        return {"code": "error", "message": e}


@bp.route("/getProductBySearch", methods=["GET", "POST"])
def get_product_by_search():
    product_name = request.args.get('search', "")
    page = int(request.args.get("currentPage", "1"))
    page_size = int(request.args.get("pageSize", "16"))
    try:
        products = get_product_by_name(product_name, page_size, page)
        product_json = [Product(**x).to_json() for x in products]
        total_product = get_product_name_total(product_name)
        return {"Product": product_json, "total": total_product}
    except Exception as e:
        return {"code": "error", "message": e}


@bp.route("/getDetails", methods=["GET", "POST"])
def get_details():
    product_id = request.args.get("productID", "")
    try:
        products = get_product_by_id(product_id)
        product_json = [Product(**x).to_json() for x in products]
        return {"Product": product_json}
    except Exception as e:
        return {"code": "error", "message": e}


def init_app(app):
    app.register_blueprint(bp)
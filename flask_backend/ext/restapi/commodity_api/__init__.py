from flask import Blueprint, request, jsonify

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
            image = get_pic_by_product_id(product_json[i]["product_id"])
            product_json[i]["image"] = image
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
        for i in range(len(product_json)):
            product_json[i]["product_id"] = str(products[i]["_id"])
            image = get_pic_by_product_id(product_json[i]["product_id"])
            product_json[i]["image"] = image
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


@bp.route("/getDetailsPicture", methods=["GET", "POST"])
def get_details_images():
    product_id = request.args.get("productID", "")
    try:
        image = get_pic_by_product_id(product_id)
        return {"image": [image]}
    except Exception as e:
        return {"code": "error", "message": e}


@bp.route('/upload_product', methods=["POST"])
def save_image():
    if 'image' in request.files:
        image = request.files['image']
        product_name = request.form.get('product_name')

        id = upload_image(image, product_name)

        query = {
            'picture_id': id,
            'product_name': product_name,
            "product_intro": request.form.get('product_intro'),
            "product_price": request.form.get('product_price'),
            "product_selling_price": request.form.get('product_selling_price')
        }
        status = db.good.insert_one(query)
        if status:
            return jsonify({'result': 'Image uploaded successfully'}), 201
        return jsonify({'result': 'Error occurred during uploading'}), 500
    return jsonify({'result': 'no image uploaded'}), 500


def init_app(app):
    app.register_blueprint(bp)

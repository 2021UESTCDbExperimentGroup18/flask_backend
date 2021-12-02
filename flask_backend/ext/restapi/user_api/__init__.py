from flask import Blueprint, request

from flask_backend.ext.restapi import user_api

bp = Blueprint("user_api", __name__, url_prefix="/api/users")


def init_app(app):
    app.register_blueprint(bp)


@bp.route('/user_info')
def get_user_info():
    user_id = request.args.get('user_id', "")
    return user_id


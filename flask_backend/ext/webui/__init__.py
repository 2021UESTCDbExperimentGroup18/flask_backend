from flask import Blueprint

from .views import index, only_admin, secret

bp = Blueprint("webui", __name__,
               static_url_path="/",
               template_folder="templates/frontend/dist/",
               static_folder="./templates/frontend/dist/")

bp.add_url_rule("/", view_func=index)


def init_app(app):
    app.register_blueprint(bp)

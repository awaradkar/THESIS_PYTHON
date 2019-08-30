from flask import Flask

from config import app_config
from masters import db
from masters.commodity.resources_comm import comm_api as com_blueprint

from masters.commodity.resources_deposit import comm_api as dep_blueprint
from masters.commodity.resources_login import comm_api as login_blueprint
from masters.commodity.resources_billing import comm_api as billing_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    db.init_app(app)

    app.register_blueprint(com_blueprint,url_prefix='/api/v1/commodities')

    app.register_blueprint(dep_blueprint, url_prefix='/api/v1/deposit')
    app.register_blueprint(login_blueprint, url_prefix='/api/v1/login')
    app.register_blueprint(billing_blueprint, url_prefix='/api/v1/billing')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app




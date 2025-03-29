from flask import Flask
from flask_security import SQLAlchemyUserDatastore


from configs import Config
from application.extensions import db, migrate, security, cors, jwt, ma, cache
from application.blueprints import create_all_api_resource_blueprint
from application.core.models import User, Role
from .routes import home_bp
from .errors import error_bp


def create_app(main_file: str, config_obj: Config) -> Flask:
    app = Flask(main_file, template_folder=config_obj.TEMPLATES_FOLDER, static_folder=config_obj.STATIC_FOLDER)

    app.config.from_object(config_obj)

    cors.init_app(
        app=app, 
        resources={r"/api/*": {'origins': config_obj.ALLOWED_ORIGINS}}, 
        allow_headers=['Content-Type', 'Authorization']
    )

    db.init_app(app)

    migrate.init_app(app, db, directory=config_obj.MIGRATE_FOLDER)

    jwt.init_app(app)
    
    ma.init_app(app)

    cache.init_app(app)
    
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore, register_blueprint=False)
    app.security = security

    app.app_context().push()

    with app.app_context():
        import application.commands
        import application.models
        db.create_all()


    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(error_bp)
    
    api_resource_bp = create_all_api_resource_blueprint(main_file)
    app.register_blueprint(api_resource_bp, url_prefix='/api/v1')
    return app
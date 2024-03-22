from flask import Flask, render_template
from .extensions import db
from .import views, auth



def load_app():

    app = Flask(__name__)

    #config proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    )

    db.init_app(app)
    
    from .import models

    #registro de las views
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template("login.html")
    
    with app.app_context():
        db.create_all()
    
    return app
from flask import Flask
from config import Config
from models.models import db
from routes.routes import bp as main_bp


def create_app():
    # 👇 make static folder explicit
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=5500)


from flask import Flask
from flask_migrate import Migrate
from api import blueprint
from model.base import db

app = Flask(__name__)

app.register_blueprint(blueprint, url_prefix="/v1")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/renso"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.app_context().push()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

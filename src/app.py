from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api import blueprint
from configuration import configs
from model.base import db

app = Flask(__name__, static_folder="../static")

app.register_blueprint(blueprint, url_prefix="/api/v1/")

app.config["CORS_HEADERS"] = "Content-Type"

app.config["SQLALCHEMY_DATABASE_URI"] = configs.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', ["https://schlei.renso.de", "https://rad.renso.de",
                                                         "https://renso.de",
                                                         "http://localhost:8080/", "http://localhost:8081/"])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,HEAD,OPTIONS')
    return response


CORS(app, resources={r'/*': {'origins': configs.ORIGINS}}, supports_credentials=True)
CORS(app)

app.app_context().push()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

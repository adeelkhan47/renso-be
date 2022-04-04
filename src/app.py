from flask import Flask, request, make_response
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
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response


CORS(app, resources={r'/*': {'origins': configs.ORIGINS}}, supports_credentials=True)

app.app_context().push()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

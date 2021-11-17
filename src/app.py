from flask import Flask
from api import blueprint
app = Flask(__name__)

app.register_blueprint(blueprint, url_prefix="/v1")

if __name__ == '__main__':
    app.run()

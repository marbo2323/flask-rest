from flask import Flask

import config
import models
from resources.courses import courses_api
from resources.reviews import reviews_api
from resources.users import users_api

API_PREFIX = "/api/v1"

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.register_blueprint(courses_api)
app.register_blueprint(reviews_api, url_prefix=API_PREFIX)
app.register_blueprint(users_api, url_prefix=API_PREFIX)


@app.route('/')
def hello_world():
    return 'Hello world!'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

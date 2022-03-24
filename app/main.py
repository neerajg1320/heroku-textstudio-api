from flask import Flask, send_from_directory
from flask_cors import CORS
from app.home_blueprint import home_blueprint
from app.regex_blueprint import regex_blueprint
from app.files_blueprint import files_blueprint
from app.middleware.simple_delay_middleware import middleware

app = Flask("REGEX")
CORS(app)

app.wsgi_app = middleware(app.wsgi_app, 0)

app.register_blueprint(regex_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(files_blueprint)

DEBUG = False

if __name__ == "__main__":
    app.run(debug=DEBUG)
from flask import Flask, send_from_directory
from flask_cors import CORS
from example_blueprint import example_blueprint
from regex_blueprint import regex_blueprint
from files_blueprint import files_blueprint
from middleware.simple_delay_middleware import middleware

app = Flask("REGEX")
CORS(app)

app.wsgi_app = middleware(app.wsgi_app, 0)

app.register_blueprint(regex_blueprint)
app.register_blueprint(files_blueprint)
app.register_blueprint(example_blueprint)

DEBUG = False

if __name__ == "__main__":
    app.run(debug=DEBUG)
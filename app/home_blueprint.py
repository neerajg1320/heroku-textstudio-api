from flask import Blueprint


home_blueprint = Blueprint('home_blueprint', __name__)


html_str = """
<h1>TextStudio Application</h1>
<h3>Running on heroku</h3>
"""

@home_blueprint.route('/')
def index():
    return html_str

from flask import Blueprint
from flask import Flask, request, jsonify

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from app.utils.debug_utils import debug_log
from app.utils.df_utils import create_df_from_text_using_regex, is_dataframe
import json  



from app.utils.regex_utils import check_compile_regex, regex_apply_on_text
from app.regex_style import create_colored_html_div
from app.exceptions import InvalidParams

regex_blueprint = Blueprint('regex_blueprint', __name__)

DEBUG = False 

app = Flask("REGEX")

def get_validated_json(request, schema):
    if request.content_type is None or not 'application/json' in request.content_type:
        raise InvalidParams("Error! json data missing")

    request_data = request.get_data().decode('utf-8') 
    # When done from react-frontend escaping is not needed
    # Excaping is needed when request is sent from Postman 
    # request_data = request_data.replace("\\", "\\\\")
    

    # Do not use request.get_json() as it throws error in case of newline in string
    # Since we allow newline in string, we use strict=False. 
      
    try:
        request_dict = json.loads(request_data, strict=False)
    except json.decoder.JSONDecodeError as e:
        raise InvalidParams(str(e))
    
    if request_dict is None:
        raise InvalidParams('Error! json body is missing')

    # This will raise ValidationError in case the request is different from schema
    validate(request_dict, schema)

    return request_dict


def create_response(result=None, error=None, status=None):
    if error is not None:
        response = (jsonify({ "status": "failed", "error": error }), 
                    status if status is not None else 400)
    else:
        response = (jsonify({"status": "success", "result": result}),
                    status if status is not None else 200)

    debug_log("response:", result if error is None else error, active=False)
    return response

@regex_blueprint.before_request
def log_request_info():
    headers = request.headers
    body = request.get_data().decode('utf-8')
    body = body.replace("\\n", "\n")

    app.logger.debug('\nHeaders: %s', headers)
    app.logger.debug('\nBody: %s', body)
    # app.logger.debug('\nBody[Hex]: %s', body.hex())
    
    with open("request.json", "w") as f:
        f.write(body)
    
    # with open("request.json", "a") as f:
    #     f.write(body.hex())

@regex_blueprint.errorhandler(InvalidParams)
def handle_invalid_params(error):
    return create_response(error=error.message)


@regex_blueprint.errorhandler(ValidationError)
def handle_validation_error(error):
    return create_response(error=error.message)

regex_is_valid_schema = {
   'type': 'object',
   'properties': {
       'name': { 'type': 'string' },
       'regex': { 'type': 'string' },
       'flags': { 'type': 'object' }
   },
   'required': ['regex']
}

@regex_blueprint.route('/regex/isValid', methods=['POST'])
def regex_isvalid():
    request_dict = get_validated_json(request, regex_is_valid_schema)

    _, regex_error = check_compile_regex(request_dict["regex"])

    result = {
        'isValid': regex_error is None
    }
    if regex_error is not None:
        result.update({'regex_error': regex_error})
    
    return create_response(result=result)


regex_apply_schema = {
    'type': 'object',
   'properties': {
       'regex': { 'type': 'string' },
       'text': {'type': 'string'},
       'flags': { 'type': 'object' }
   },
   'required': ['regex', 'text']
}

@regex_blueprint.route('/regex/apply', methods=['POST'])
def regex_apply():
    request_dict = get_validated_json(request, regex_apply_schema)

    regex_str = request_dict["regex"]
    text = request_dict["text"]
    flags = request_dict.get("flags", None)

    if DEBUG:        
        print("Regex Str:\n", regex_str)
        print("Text:\n", text)
        print("Flags:\n", flags)

    result = regex_apply_on_text(regex_str, text, flags=flags)

    return create_response(result=result, error=result["error"], status=200)

@regex_blueprint.route('/regex/dataframe', methods=['POST'])
def regex_dataframe():
    request_dict = get_validated_json(request, regex_apply_schema)

    regex_str = request_dict["regex"]
    text = request_dict["text"]
    flags = request_dict.get("flags", None)

    if DEBUG:        
        print("Regex Str:\n", regex_str)
        print("Text:\n", text)
        print("Flags:\n", flags)

    df = create_df_from_text_using_regex(regex_str, text, flags=flags)
    debug_log("regex_dataframe(): dataframe({})".format(type(df)), active=False)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
    # debug_pretty_json(json.loads(df.to_json(orient="records")))
    table = None
    if is_dataframe(df):
        table = json.loads(df.to_json(orient="table"))
        # debug_pretty_json(table)
    else:
        debug_log("Warning: table is None.")


    result = {"table": table, "error": None}
    
    return create_response(result=result, error=result["error"], status=200)


@regex_blueprint.route('/regex/html', methods=['POST'])
def regex_apply_html():
    request_dict = get_validated_json(request, regex_apply_schema)

    regex_str = request_dict["regex"]
    text = request_dict["text"]
    flags = request_dict.get("flags", None)

    if DEBUG:
        print("Regex Str:\n", regex_str)
        print("Text:\n", text)
        print("Flags:\n", flags)

    # https://www.materialpalette.com/colors
    colors = ['#c5cae9', '#ce93d8', '#4db6ac', '#9fa8da', '#ffccbc', "#7986cb", "#b2ebf2"]
    html_str = create_colored_html_div(text, regex_str, colors)

    result = {
        'html': html_str
    }
    return create_response(result=result)


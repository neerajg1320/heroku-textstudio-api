import re
import pandas as pd
from app.utils.regex_utils import check_compile_regex

def is_dataframe(var):
    return isinstance(var, pd.DataFrame)

def create_df_from_text_using_regex(regex_text, input_file_text, flags=None):
    # error = None
    # print("Regex Text: ", regex_text)
    # print("Error: ", error)
    
    p, error = check_compile_regex(regex_text, flags=flags)
    
    if error:
        print("Regex has errors: ", error)
        return None

    s = pd.Series(input_file_text)
    df = pd.DataFrame()
    try:
        df = s.str.extractall(regex_text , re.MULTILINE)
    except ValueError as e:
        print(e)

    return df
    
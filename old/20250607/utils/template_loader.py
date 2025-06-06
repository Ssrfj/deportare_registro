import pandas as pd
import logging
from config.paths import CHECK_TEMPLATE_FILE

def load_check_template_paper1(path="templates/check_paper1_registration_criteria_confirmation_formtemplate_R6.xlsx"):
    try:
        df = pd.read_excel(path, sheet_name=0)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.exception("書類①テンプレートの読み込みに失敗しました")
        return []

def load_check_template_paper2_1(path="templates/check_paper2_1_template.xlsx"):
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.exception("書類②-1テンプレートの読み込みに失敗しました")
        return []

def load_check_template_paper2_2(path="templates/check_paper2_2_template.xlsx"):
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.exception("書類②-2テンプレートの読み込みに失敗しました")
        return []

def load_check_template_paper3(path="templates/check_paper3_template.xlsx"):
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.exception("書類③テンプレートの読み込みに失敗しました")
        return []
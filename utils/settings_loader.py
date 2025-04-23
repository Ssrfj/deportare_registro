import json

def load_settings(path="config/settings.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        import logging
        logging.exception("設定ファイルの読み込みに失敗しました")
        return {}

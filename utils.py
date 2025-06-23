from datetime import datetime, timezone, timedelta

def get_jst_now():
    """
    日本標準時（JST）の現在時刻を返す。
    """
    return datetime.now(timezone(timedelta(hours=9)))

def make_checklist_filename(club_name, application_date_str):
    """
    クラブ名・申請日・作成日からチェックリスト用のファイル名を生成する。
    """
    club_name = str(club_name).strip()
    return f"{club_name}_申請{application_date_str}.xlsx"
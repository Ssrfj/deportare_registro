def make_chacklists():
    import os
    import pandas as pd
    import logging
    from setting import content_check_folder_path, application_statues_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")
'''今後の作業memo
作るファイル
（総合の）チェックリスト
書類ごとのチェックリスト
一貫性のチェックリスト
基準に適合しているかのチェックリスト
クラブごと＊書類ごとの詳細なデータ

※ファイルについては処理ごとに、また別のPythonファイルを作る

作るフォルダ
クラブごとの詳細データ保存フォルダ
'''
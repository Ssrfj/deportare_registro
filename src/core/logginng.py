# logging.py
# 機能：「実行ごと」のログと複数回の実行でのログを分けるための設定
def setup_logging():
    """ロギングの設定"""
    import os
    import logging
    from setting_paths import log_folder_path
    
    # ログフォルダの作成
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    # 既存のハンドラーをクリア
    logging.getLogger().handlers.clear()
    
    # UTF-8エンコーディングでファイルハンドラーを作成
    log_file_path = os.path.join(log_folder_path, 'reception.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # フォーマッターの設定
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    logging.info("ロギングを設定しました")


def read_log_with_detected_encoding(filepath):
    """ログファイルのエンコーディングを自動検出して読み込む関数"""
    import chardet
    with open(filepath, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding']
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()


def save_logs():
    """個別実行ログと統合ログの両方を保存する"""
    import os
    import logging
    from setting_paths import output_main_folder_path, log_folder_name
    from utils import get_jst_now
    
    logging.info("ログファイルの保存を開始します")
    log_folder_path = os.path.join(output_main_folder_path, log_folder_name)
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
        logging.info(f"ログフォルダを作成しました: {log_folder_path}")
    else:
        logging.info(f"ログフォルダは既に存在します: {log_folder_path}")
    
    # 現在のログ内容を取得
    current_log_content = ""
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            try:
                current_log_content += read_log_with_detected_encoding(handler.baseFilename)
            except Exception as e:
                current_log_content += f"\n[ログ読込エラー: {e}]\n"
    
    # 1. 個別実行ログファイルの保存
    timestamp = get_jst_now().strftime("%Y%m%d%H%M%S")
    individual_log_file_path = os.path.join(log_folder_path, f'log_{timestamp}.txt')
    os.makedirs(os.path.dirname(individual_log_file_path), exist_ok=True)
    
    with open(individual_log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"=== 実行ログ（{get_jst_now().strftime('%Y年%m月%d日 %H:%M:%S')}実行分） ===\n\n")
        log_file.write(current_log_content)
    logging.info(f"個別実行ログファイルを保存しました: {individual_log_file_path}")
    
    # 2. 統合ログファイル（過去のログと結合）の保存
    integrated_log_file_path = os.path.join(log_folder_path, 'integrated_log.txt')
    
    # 既存の統合ログがあれば読み込み
    existing_integrated_log = ""
    if os.path.exists(integrated_log_file_path):
        try:
            existing_integrated_log = read_log_with_detected_encoding(integrated_log_file_path)
        except Exception as e:
            logging.warning(f"既存の統合ログファイル読み込みでエラー: {e}")
            existing_integrated_log = f"[既存ログ読込エラー: {e}]\n\n"
    
    # 統合ログファイルに今回分を追加
    with open(integrated_log_file_path, 'w', encoding='utf-8') as integrated_log_file:
        # 既存のログがあれば先に書き込み
        if existing_integrated_log:
            integrated_log_file.write(existing_integrated_log)
            integrated_log_file.write("\n" + "="*80 + "\n\n")
        
        # 今回の実行ログを追加
        integrated_log_file.write(f"=== 実行ログ（{get_jst_now().strftime('%Y年%m月%d日 %H:%M:%S')}実行分） ===\n\n")
        integrated_log_file.write(current_log_content)
        integrated_log_file.write("\n\n")
    
    logging.info(f"統合ログファイル（過去のログと結合）を更新しました: {integrated_log_file_path}")
    logging.info("ログファイルの保存が完了しました")

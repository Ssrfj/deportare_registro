import os
import logging
from config.paths import LOGS_DIR

def save_log(club_name, result_row, messages=None):
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{club_name}_log.txt")

    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"📌 提出状況ログ（クラブ名: {club_name}）\n")
            f.write("=" * 40 + "\n")
            for key, value in result_row.items():
                if key != "クラブ名":
                    f.write(f"{key}: {value}\n")

            if messages:
                f.write("\n📋 指摘事項:\n")
                for msg in messages:
                    f.write(f" - {msg}\n")

        logging.info(f"{club_name}: ログファイルを出力しました → {log_path}")

    except Exception as e:
        logging.exception(f"{club_name}: ログファイルの出力に失敗しました")

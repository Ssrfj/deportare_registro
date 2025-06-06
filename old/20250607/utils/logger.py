import os
import logging
from config.paths import PROCESS_LOG_FILE

def setup_logging():
    os.makedirs(os.path.dirname(PROCESS_LOG_FILE), exist_ok=True)

    logging.basicConfig(
        filename=PROCESS_LOG_FILE,
        filemode='a',
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )

    # コンソールにもログを出したい場合（任意）
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info("🔧 ログ設定を初期化しました。")

"""
Outlook機能のテスト用スクリプト
"""

import os
import logging
from datetime import datetime

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_outlook_functionality():
    """Outlookの基本機能をテスト"""
    
    print("=== Outlookテスト開始 ===")
    
    # 1. win32com.clientのインポートテスト
    try:
        import win32com.client
        print("✅ win32com.clientのインポート成功")
        logging.info("win32com.clientのインポート成功")
    except Exception as e:
        print(f"❌ win32com.clientのインポート失敗: {e}")
        logging.error(f"win32com.clientのインポート失敗: {e}")
        return False
    
    # 2. Outlookアプリケーションへの接続テスト
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        print("✅ Outlookアプリケーションへの接続成功")
        logging.info("Outlookアプリケーションへの接続成功")
    except Exception as e:
        print(f"❌ Outlookアプリケーションへの接続失敗: {e}")
        logging.error(f"Outlookアプリケーションへの接続失敗: {e}")
        return False
    
    # 3. メールアイテムの作成テスト
    try:
        mail_item = outlook.CreateItem(0)  # 0 = olMailItem
        print("✅ メールアイテムの作成成功")
        logging.info("メールアイテムの作成成功")
    except Exception as e:
        print(f"❌ メールアイテムの作成失敗: {e}")
        logging.error(f"メールアイテムの作成失敗: {e}")
        return False
    
    # 4. メールプロパティの設定テスト
    try:
        mail_item.Subject = "テストメール"
        mail_item.Body = "これはテスト用のメールです。"
        print("✅ メールプロパティの設定成功")
        logging.info("メールプロパティの設定成功")
    except Exception as e:
        print(f"❌ メールプロパティの設定失敗: {e}")
        logging.error(f"メールプロパティの設定失敗: {e}")
        return False
    
    # 5. ファイル保存テスト
    try:
        test_folder = "test_outlook_output"
        os.makedirs(test_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_file_path = os.path.join(test_folder, f"test_mail_{timestamp}.msg")
        
        print(f"保存先パス: {test_file_path}")
        logging.info(f"保存先パス: {test_file_path}")
        
        # 絶対パスに変換
        abs_test_file_path = os.path.abspath(test_file_path)
        print(f"絶対パス: {abs_test_file_path}")
        logging.info(f"絶対パス: {abs_test_file_path}")
        
        mail_item.SaveAs(abs_test_file_path, 3)  # 3 = olMSG format
        
        # ファイルが実際に作成されたかチェック
        if os.path.exists(abs_test_file_path):
            print(f"✅ メールファイルの保存成功: {abs_test_file_path}")
            logging.info(f"メールファイルの保存成功: {abs_test_file_path}")
            
            # ファイルサイズも確認
            file_size = os.path.getsize(abs_test_file_path)
            print(f"   ファイルサイズ: {file_size} bytes")
            logging.info(f"ファイルサイズ: {file_size} bytes")
        else:
            print(f"❌ メールファイルが作成されていません: {abs_test_file_path}")
            logging.error(f"メールファイルが作成されていません: {abs_test_file_path}")
            return False
            
    except Exception as e:
        print(f"❌ メールファイルの保存失敗: {e}")
        logging.error(f"メールファイルの保存失敗: {e}")
        return False
    
    # 6. オブジェクトの解放テスト
    try:
        mail_item = None
        outlook = None
        print("✅ Outlookオブジェクトの解放成功")
        logging.info("Outlookオブジェクトの解放成功")
    except Exception as e:
        print(f"⚠️ Outlookオブジェクトの解放で警告: {e}")
        logging.warning(f"Outlookオブジェクトの解放で警告: {e}")
    
    print("=== Outlookテスト完了 ===")
    return True

def test_path_handling():
    """パス処理のテスト"""
    print("\n=== パス処理テスト ===")
    
    # 問題のあるパスをテスト
    problem_path = "E:\\oasobi\\deportare_registro\\output/R7_登録受付処理\\メール文面案\\メール文面案\\日本橋クラブ_メール文面案\\メール文面案_日本橋クラブ_20250723_142709.msg"
    
    print(f"問題のパス: {problem_path}")
    
    # パスの正規化
    normalized_path = os.path.normpath(problem_path)
    print(f"正規化後: {normalized_path}")
    
    # ディレクトリ部分を確認
    directory = os.path.dirname(normalized_path)
    print(f"ディレクトリ: {directory}")
    
    # ディレクトリが存在するかチェック
    if os.path.exists(directory):
        print(f"✅ ディレクトリは存在します")
    else:
        print(f"❌ ディレクトリが存在しません")
        print(f"   作成を試みます...")
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ ディレクトリを作成しました")
        except Exception as e:
            print(f"❌ ディレクトリの作成に失敗: {e}")
    
    print("=== パス処理テスト完了 ===")

if __name__ == "__main__":
    test_path_handling()
    print()
    success = test_outlook_functionality()
    
    if success:
        print("\n🎉 すべてのテストが成功しました！")
    else:
        print("\n💥 テストで問題が発見されました。")

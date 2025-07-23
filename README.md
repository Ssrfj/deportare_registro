# クラブ登録受付自動処理・チェックツール

## 概要

このリポジトリは、某SPOが運用する総合型地域スポーツクラブ登録・認証制度の登録手続きにおいて、都道府県スポーツ協会における処理を簡易化するために、受付内容や提出書類を大半を自動でチェックし、提出状況一覧等を作成するPythonツール群です。
※ただし、こちらが想定する形式でクラブに受付を求めるというイレギュラーな運用を前提にしています。
また、某京都での運用を前提にしています。

## プロジェクト構造

```
deportare_registro/
├── main.py                    # メインエントリーポイント
├── requirements.txt           # 依存関係
├── README.md                  # プロジェクトドキュメント
├── .gitignore                 # Git除外設定
├── src/                       # ソースコード
│   ├── core/                  # コア機能
│   │   ├── logginng.py        # ログ設定
│   │   ├── setting_paths.py   # パス設定
│   │   └── utils.py           # ユーティリティ関数
│   ├── data_processing/       # データ処理関連
│   │   ├── processing_reception_data.py
│   │   ├── marge_reception_data_with_club_info.py
│   │   ├── reception_statues.py
│   │   ├── column_name_change.py
│   │   └── make_detailed_club_data.py
│   ├── folder_management/     # フォルダ管理
│   │   ├── make_folders.py
│   │   └── make_detailed_data_folders.py
│   ├── checklist/            # チェックリスト関連
│   │   ├── generators/       # チェックリスト生成
│   │   │   ├── checklist_generator.py
│   │   │   ├── make_chacklists.py
│   │   │   ├── make_overall_checklist.py
│   │   │   └── documents/    # 各種書類チェックリスト生成
│   │   │       └── make_document*.py
│   │   ├── consistency/      # 整合性チェック
│   │   │   └── make_consistency_*.py
│   │   └── automation/       # 自動チェック
│   │       ├── automation_check_and_update_checklist.py
│   │       ├── auto_check.py
│   │       ├── check_functions.py
│   │       └── documents_check_functions.py
│   └── human_interface/      # 人間用インターフェース
│       ├── make_and_write_documents_checklist_for_human.py
│       └── email_draft_generator.py  # メール文面案生成
├── config/                   # 設定ファイル
│   ├── checklist_columns/   # チェックリスト設定
│   │   └── *.json
│   └── reference_data/      # 参照データ
│       └── *.csv, *.xlsx
├── data/                    # データファイル
│   ├── clubs/               # クラブデータ
│   └── applications/        # 申請データ
├── output/                  # 出力ファイル
│   └── R7_登録受付処理/     # 処理結果
└── test/                    # テストファイル
```

## 主な機能

- クラブごとのフォルダをスキャンし、提出書類を自動判定
- Excelテンプレートに基づくセル内容の自動チェック
- チェック結果の一覧（Excelファイル）を自動生成
- **エラーがあるクラブに対する個別メール文面案の自動生成**
  - テキストファイル（.txt）: 編集・バックアップ用
  - EMLファイル（.eml）: メールアプリで直接開ける標準メール形式
  - クラブ固有のエラー内容を含む個別対応メッセージ
- ログ出力による処理状況の記録

## 必要な環境

- Python 3.10 以上
- pandas
- openpyxl
- email (標準ライブラリ - メール文面案生成用)
- その他 requirements.txt に記載のライブラリ

## 使い方

1. 必要なPythonパッケージをインストールします。

    ```sh
    pip install -r requirements.txt
    ```

2. `config/paths.py` や `utils/settings_loader.py` で入力フォルダや年度などの設定を行います。

3. クラブごとの提出書類を所定のフォルダに配置します。

4. メインスクリプトを実行します。

    ```sh
    python main.py
    ```

5. チェック結果は `output/R7_登録受付処理/` 配下に出力されます。

6. エラーがあるクラブについては、メール文面案が自動生成されます。
   - EMLファイルをダブルクリックしてメールアプリで開き、内容確認後送信可能
   - 各クラブの固有エラーに応じた個別対応メッセージが生成されます

## ディレクトリ構成例

- `main.py` : メイン処理
- `src/` : ソースコード（各種ユーティリティ、チェック機能、メール文面案生成等）
- `config/` : 設定ファイル
- `data/` : 入力データ
- `output/` : 出力データ（チェックリスト、メール文面案等）

## メール文面案生成機能

### 概要
チェック結果に基づいて、エラーがあるクラブに対して個別のメール文面案を自動生成します。

### 生成されるファイル
- **テキストファイル（.txt）**: 内容の確認・編集用
- **EMLファイル（.eml）**: メールアプリで直接開ける標準形式

### 対応エラー種類
- 自動チェック結果（入力値エラー、必須項目未入力など）
- 書類間整合性チェック結果（データの不一致）
- 書類別チェック結果（各書類固有のエラー）

### 対応メールアプリ
- Windows Mail
- Microsoft Outlook
- Mozilla Thunderbird
- Apple Mail
- その他RFC822/MIME対応メールアプリ

## ライセンス

本リポジトリの内容は、利用者の責任においてご利用ください。

---

ご質問・ご要望はIssueまたはPull Requestでお知らせください。
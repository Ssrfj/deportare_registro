"""
メール文面案作成機能
GitHubのissue #24に基づいて、エラーコードから適切なメール文面案を生成する
"""

import os
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

class EmailDraftGenerator:
    """メール文面案作成クラス"""
    
    def __init__(self):
        """初期化"""
        self.error_messages = self._load_error_messages()
        self.email_template = self._get_email_template()
        logging.info("メール文面案作成機能を初期化しました")
    
    def _load_error_messages(self) -> Dict[str, Dict[str, str]]:
        """
        エラーコードとメッセージの対応表を読み込み
        """
        error_messages = {
            "e_a_000": {
                "content": "入力が必須な項目が未入力です。{該当箇所}",
                "action": "入力・修正のうえ再度提出をお願いします。"
            },
            "e_a_001": {
                "content": "貴クラブは、東京都に設立の届出をしておらず、その際に必須となる届出中であることが確認できる書類も提出していません。",
                "action": "届出中であることを確認できる書類を提出するか、所在区市町村のスポーツ主管課を通じて東京都に届出をご提出ください。"
            },
            "e_a_002": {
                "content": "当協会で把握している所在区市町村と申請していただいた区市町村が異なります。",
                "action": "入力内容に問題が無いかをご確認いただくか、東京都への申請に問題が無いかをご確認ください。"
            },
            "e_a_003-a": {
                "content": "電話番号が異常な値です。",
                "action": "入力内容に問題が無いかをご確認ください。"
            },
            "e_a_003-b": {
                "content": "電話番号が入力されていません。",
                "action": "入力の上、ご提出ください。"
            },
            "e_a_004-a": {
                "content": "FAX番号が異常な値です。",
                "action": "入力内容に問題が無いかをご確認ください。"
            },
            "e_a_004-b": {
                "content": "FAX番号が入力されていません。",
                "action": "入力の上、ご提出ください。"
            },
            "e_a_005-a": {
                "content": "申請種別が「新規」となっていますが、貴クラブはR7年度に登録済みのため、申請種別は「更新」です。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_005-b": {
                "content": "申請種別が「更新」となっていますが、貴クラブはR7年度に登録されていないため、申請種別は「新規」です。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_005-c": {
                "content": "内部エラー",
                "action": "内部エラー"
            },
            "e_a_005-d": {
                "content": "内部エラー",
                "action": "内部エラー"
            },
            "e_a_005-e": {
                "content": "内部エラー",
                "action": "内部エラー"
            },
            "e_a_006-a": {
                "content": "登録基準に適合していないと申請しています。{該当箇所}",
                "action": "登録基準と申請内容をご確認いただき、必要があれば、修正の上、再度提出をお願いします。"
            },
            "e_a_007-a": {
                "content": "会員数の入力欄に数字ではないデータが入力されています。{該当箇所}",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_007-b": {
                "content": "年会費等を支払っている会員数の入力欄に数字ではないデータが入力されています。{該当箇所}",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_008-a": {
                "content": "定期的なスポーツ活動を2種目以上行っていない。{入力種目数}",
                "action": "活動実態と申請内容をご確認いただき、必要があれば、修正の上、再度提出をお願いします。"
            },
            "e_a_008-b": {
                "content": "選択肢にない活動種目の数を入力する項目に数字が入力されていません。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_010-a": {
                "content": "マネジメント指導者数の入力欄に数字ではないデータが入力されています。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_011-a": {
                "content": "規約等の改廃を決議した際の議事録が提出されていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_011-b": {
                "content": "改正前の規約等が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_012-a": {
                "content": "貴クラブは、新規登録クラブです。必須書類である規約等の提出がされていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_012-b": {
                "content": "貴クラブは、更新クラブですが、規約等を改正したクラブです。しかし、必須書類である改定後の規約等が提出されていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_012-c": {
                "content": "規約等の提出がされてません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_013-a": {
                "content": "貴クラブは、新規登録クラブです。必須書類である役員名簿（議決権保有者の名簿）の提出がされていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_013-b": {
                "content": "貴クラブは、更新クラブですが、役員名簿（議決権保有者の名簿）を「提出する」と入力しています。しかし、役員名簿（議決権保有者の名簿）の提出がされていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_013-c": {
                "content": "役員名簿（議決権保有者名簿）の提出がされていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_014-a": {
                "content": "事業計画が提出されていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_014-b": {
                "content": "事業計画を決議した際の議事録が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_015-a": {
                "content": "予算が提出されていません。",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_015-b": {
                "content": "予算を決議した際の議事録が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_016-a": {
                "content": "貴クラブは、昨年度以前に設立されたクラブです。そのため事業報告の提出が必須です。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_016-b": {
                "content": "事業報告が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_016-c": {
                "content": "事業報告を決議した際の議事録が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_017-a": {
                "content": "貴クラブは、昨年度以前に設立されたクラブです。そのため決算の提出が必須です。",
                "action": "修正の上、再度提出をお願いします。"
            },
            "e_a_017-b": {
                "content": "決算が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            "e_a_017-c": {
                "content": "決算を決議した際の議事録が提出されていません",
                "action": "入力内容に問題が無いかをご確認いただくか、必要書類をご提出ください。"
            },
            # 書類チェック用エラーコード
            "e_d_001": {
                "content": "書類01（申請書）にエラーがあります。{該当箇所}",
                "action": "申請書の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_002_1": {
                "content": "書類02-1（規約等）にエラーがあります。{該当箇所}",
                "action": "規約等の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_002_2": {
                "content": "書類02-2（規約等の議事録）にエラーがあります。{該当箇所}",
                "action": "規約等の議事録の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_003": {
                "content": "書類03（役員名簿）にエラーがあります。{該当箇所}",
                "action": "役員名簿の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_004": {
                "content": "書類04（自己点検シート）にエラーがあります。{該当箇所}",
                "action": "自己点検シートの内容をご確認いただき、修正をお願いします。"
            },
            "e_d_005_budget": {
                "content": "書類05（予算書）にエラーがあります。{該当箇所}",
                "action": "予算書の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_005_plan": {
                "content": "書類05（事業計画書）にエラーがあります。{該当箇所}",
                "action": "事業計画書の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_006_report": {
                "content": "書類06（事業報告書）にエラーがあります。{該当箇所}",
                "action": "事業報告書の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_006_financial": {
                "content": "書類06（決算書）にエラーがあります。{該当箇所}",
                "action": "決算書の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_007": {
                "content": "書類07（事業計画の議事録）にエラーがあります。{該当箇所}",
                "action": "事業計画の議事録の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_008": {
                "content": "書類08（予算の議事録）にエラーがあります。{該当箇所}",
                "action": "予算の議事録の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_009": {
                "content": "書類09（事業報告の議事録）にエラーがあります。{該当箇所}",
                "action": "事業報告の議事録の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_010": {
                "content": "書類10（決算の議事録）にエラーがあります。{該当箇所}",
                "action": "決算の議事録の内容をご確認いただき、修正をお願いします。"
            },
            "e_d_incomplete": {
                "content": "書類のチェックが完了していません。{該当箇所}",
                "action": "必要書類をご提出いただき、チェックの完了をお待ちください。"
            }
        }
        
        logging.info(f"エラーメッセージ定義を読み込みました: {len(error_messages)}件")
        return error_messages
    
    def _get_email_template(self) -> str:
        """
        メールテンプレートを取得
        """
        template = """件名：令和8年度登録認証制度　登録申請内容について

{club_name}{contact_person_title}　{contact_person_name}様

いつもお世話になっております。○県スポーツ協会の○○と申します。

この度は令和7年度登録認証制度にご申請いただきありがとうございました。登録申請内容を確認させていただき、以下の事項について、ご確認・ご対応をお願いしたくご連絡いたしました。

{error_details}

お手数をおかけしますが、どうぞよろしくお願いいたします。"""
        
        return template
    
    def generate_email_draft(self, 
                           club_name: str,
                           contact_person_name: str,
                           contact_person_title: str,
                           error_codes: List[str],
                           error_details: Dict[str, str] = None) -> str:
        """
        メール文面案を生成
        
        Args:
            club_name: クラブ名
            contact_person_name: 申請担当者名
            contact_person_title: 申請担当者役職
            error_codes: エラーコードのリスト
            error_details: エラーの詳細情報（該当箇所などの追加情報）
            
        Returns:
            生成されたメール文面案
        """
        try:
            if not error_codes:
                logging.warning("エラーコードが提供されていません")
                return None
            
            # エラー詳細を組み立て
            error_sections = []
            for i, error_code in enumerate(error_codes, 1):
                if error_code not in self.error_messages:
                    logging.warning(f"未知のエラーコード: {error_code}")
                    continue
                
                error_info = self.error_messages[error_code]
                error_content = error_info["content"]
                error_action = error_info["action"]
                
                # 詳細情報の挿入（該当箇所などの情報）
                if error_details and error_code in error_details:
                    detail_info = error_details[error_code]
                    if "{該当箇所}" in error_content:
                        if detail_info.strip():  # 空でない場合のみ置換
                            error_content = error_content.replace("{該当箇所}", detail_info)
                        else:
                            error_content = error_content.replace("{該当箇所}", "")
                    if "{入力種目数}" in error_content:
                        error_content = error_content.replace("{入力種目数}", detail_info)
                else:
                    # 詳細情報がない場合は{該当箇所}を空文字に置換
                    if "{該当箇所}" in error_content:
                        error_content = error_content.replace("{該当箇所}", "")
                    if "{入力種目数}" in error_content:
                        error_content = error_content.replace("{入力種目数}", "")
                
                error_section = f"【確認事項{i}】\n{error_content}\n\n【対応依頼】\n{error_action}"
                error_sections.append(error_section)
            
            # エラー詳細を結合
            error_details_text = "\n\n".join(error_sections)
            
            # メール文面を生成
            email_draft = self.email_template.format(
                club_name=club_name,
                contact_person_name=contact_person_name,
                contact_person_title=contact_person_title,
                error_details=error_details_text
            )
            
            logging.info(f"クラブ '{club_name}' のメール文面案を生成しました（エラー数: {len(error_codes)}）")
            return email_draft
            
        except Exception as e:
            logging.error(f"メール文面案の生成中にエラーが発生しました: {e}")
            return None
    
    def extract_errors_from_document_check(self, document_check_result: str) -> Tuple[List[str], Dict[str, str]]:
        """
        書類チェック結果からエラーコードを抽出
        
        Args:
            document_check_result: 書類チェック結果（文字列形式）
            
        Returns:
            Tuple[List[str], Dict[str, str]]: エラーコードのリストと詳細情報
        """
        error_codes = []
        error_details = {}
        
        if not document_check_result or pd.isna(document_check_result):
            return error_codes, error_details
            
        try:
            # 書類チェック結果を解析
            # 形式例: "書類01:エラー有{クラブ名,住所,担当者名}:yamada,書類02-1:エラー有{申請種別,申請担当者名}:チェックが完了していません"
            
            # カンマで分割して各書類のチェック結果を取得
            document_checks = str(document_check_result).split(',')
            
            for check in document_checks:
                check = check.strip()
                if not check:
                    continue
                    
                try:
                    # 書類番号を抽出
                    if ':' not in check:
                        continue
                        
                    parts = check.split(':')
                    if len(parts) < 2:
                        continue
                        
                    document_type = parts[0].strip()
                    status_info = ':'.join(parts[1:])
                    
                    # エラー有の場合のみ処理
                    if 'エラー有' in status_info:
                        # エラーコードを生成
                        error_code = self._get_document_error_code(document_type, status_info)
                        if error_code:
                            error_codes.append(error_code)
                            
                            # 詳細情報を抽出
                            error_detail = self._extract_document_error_detail(document_type, status_info)
                            if error_detail:
                                error_details[error_code] = error_detail
                                
                except Exception as e:
                    logging.warning(f"書類チェック結果の解析でエラー: {check} - {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"書類チェック結果の解析中にエラーが発生しました: {e}")
            
        return error_codes, error_details
    
    def _get_document_error_code(self, document_type: str, status_info: str) -> str:
        """
        書類タイプとステータス情報からエラーコードを生成
        """
        try:
            # チェックが完了していない場合
            if 'チェックが完了していません' in status_info:
                return 'e_d_incomplete'
                
            # 書類タイプに応じてエラーコードを決定
            if document_type == '書類01':
                return 'e_d_001'
            elif document_type == '書類02-1':
                return 'e_d_002_1'
            elif document_type == '書類02-2':
                return 'e_d_002_2'
            elif document_type == '書類03':
                return 'e_d_003'
            elif document_type == '書類04':
                return 'e_d_004'
            elif document_type == '書類05予算':
                return 'e_d_005_budget'
            elif document_type == '書類05計画':
                return 'e_d_005_plan'
            elif document_type == '書類06報告':
                return 'e_d_006_report'
            elif document_type == '書類06決算':
                return 'e_d_006_financial'
            elif document_type == '書類07':
                return 'e_d_007'
            elif document_type == '書類08':
                return 'e_d_008'
            elif document_type == '書類09':
                return 'e_d_009'
            elif document_type == '書類10':
                return 'e_d_010'
            else:
                logging.warning(f"未知の書類タイプ: {document_type}")
                return None
                
        except Exception as e:
            logging.error(f"書類エラーコードの生成中にエラー: {e}")
            return None
    
    def _extract_document_error_detail(self, document_type: str, status_info: str) -> str:
        """
        書類のエラー詳細情報を抽出
        """
        try:
            # エラー有{...}の中身を抽出
            if '{' in status_info and '}' in status_info:
                start = status_info.find('{')
                end = status_info.find('}')
                if start < end:
                    error_fields = status_info[start+1:end]
                    return error_fields
            return ""
        except Exception as e:
            logging.error(f"書類エラー詳細の抽出中にエラー: {e}")
            return ""

    def extract_errors_from_auto_check(self, auto_check_result, inter_document_check_result) -> Tuple[List[str], Dict[str, str]]:
        """
        自動チェック結果と書類間チェック結果からエラーコードを抽出
        
        Args:
            auto_check_result: 自動チェック結果（JSON形式またはdict）
            inter_document_check_result: 書類間チェック結果（JSON形式またはdict）
            
        Returns:
            エラーコードのリストと詳細情報の辞書
        """
        try:
            error_codes = []
            error_details = {}
            
            # 自動チェック結果の処理
            auto_dict = self._parse_check_result(auto_check_result)
            if auto_dict:
                for error_code, error_message in auto_dict.items():
                    if error_code.startswith('e_') and error_code in self.error_messages:
                        error_codes.append(error_code)
                        # エラーメッセージから詳細情報を抽出
                        if ":" in str(error_message):
                            detail_part = str(error_message).split(":", 1)[1].strip()
                            error_details[error_code] = detail_part
            
            # 書類間チェック結果の処理
            inter_dict = self._parse_check_result(inter_document_check_result)
            if inter_dict:
                for error_code, error_message in inter_dict.items():
                    if error_code.startswith('e_') and error_code in self.error_messages:
                        error_codes.append(error_code)
                        # エラーメッセージから詳細情報を抽出
                        if ":" in str(error_message):
                            detail_part = str(error_message).split(":", 1)[1].strip()
                            error_details[error_code] = detail_part
            
            logging.info(f"抽出されたエラーコード: {error_codes}")
            return error_codes, error_details
            
        except Exception as e:
            logging.error(f"自動チェック結果からのエラー抽出中にエラーが発生しました: {e}")
            return [], {}
    
    def _parse_check_result(self, check_result) -> Dict:
        """
        チェック結果をdictionary形式に変換
        
        Args:
            check_result: チェック結果（dict、JSON文字列、またはその他）
            
        Returns:
            解析済みのdictionary
        """
        try:
            if isinstance(check_result, dict):
                return check_result
            elif isinstance(check_result, str):
                # JSON文字列として解析を試行
                try:
                    # シングルクォートをダブルクォートに変換
                    normalized_str = check_result.replace("'", '"')
                    return json.loads(normalized_str)
                except json.JSONDecodeError:
                    # evalで辞書として解析を試行（安全でないが、制御された環境なので）
                    try:
                        return eval(check_result)
                    except:
                        logging.warning(f"チェック結果の解析に失敗しました: {check_result}")
                        return {}
            else:
                logging.warning(f"予期しないチェック結果の形式: {type(check_result)}")
                return {}
        except Exception as e:
            logging.error(f"チェック結果の解析中にエラーが発生しました: {e}")
            return {}

    def extract_errors_from_checklist(self, checklist_result: str) -> Tuple[List[str], Dict[str, str]]:
        """
        チェックリスト結果からエラーコードを抽出
        
        Args:
            checklist_result: チェックリストの結果文字列
            
        Returns:
            エラーコードのリストと詳細情報の辞書
        """
        try:
            error_codes = []
            error_details = {}
            
            # 簡潔形式の場合: "書類01:エラー有{申請種別,申請担当者名}:チェック者"
            if "エラー有" in checklist_result:
                # エラー内容の抽出
                if "{" in checklist_result and "}" in checklist_result:
                    start = checklist_result.find("{")
                    end = checklist_result.find("}", start)
                    error_content = checklist_result[start+1:end]
                    
                    # エラー内容からエラーコードを推定
                    # この部分は実際のチェックリスト結果の形式に合わせて調整が必要
                    if "申請種別" in error_content:
                        error_codes.extend(["e_a_005-a", "e_a_005-b"])  # 申請種別関連
                    if "申請担当者名" in error_content:
                        error_codes.append("e_a_000")
                        error_details["e_a_000"] = "申請担当者名"
                    if "電話番号" in error_content:
                        error_codes.extend(["e_a_003-a", "e_a_003-b"])
                    if "FAX番号" in error_content:
                        error_codes.extend(["e_a_004-a", "e_a_004-b"])
            
            return error_codes, error_details
            
        except Exception as e:
            logging.error(f"チェックリスト結果からのエラー抽出中にエラーが発生しました: {e}")
            return [], {}
    
    def save_email_draft(self, email_draft: str, club_name: str, output_folder: str) -> str:
        """
        メール文面案をファイルに保存
        
        Args:
            email_draft: メール文面案
            club_name: クラブ名
            output_folder: 出力フォルダパス
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # ファイル名の生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"メール文面案_{club_name}_{timestamp}.txt"
            
            # 出力フォルダの作成
            os.makedirs(output_folder, exist_ok=True)
            
            # ファイルパスの生成
            file_path = os.path.join(output_folder, filename)
            
            # ファイルに保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(email_draft)
            
            logging.info(f"メール文面案を保存しました: {file_path}")
            return file_path
            
        except Exception as e:
            logging.error(f"メール文面案の保存中にエラーが発生しました: {e}")
            return None
    
    def generate_bulk_email_drafts(self, checklist_df: pd.DataFrame, output_folder: str) -> Dict[str, str]:
        """
        総合チェックリストから複数クラブのメール文面案を一括生成
        
        Args:
            checklist_df: 総合チェックリストのDataFrame
            output_folder: 出力フォルダパス
            
        Returns:
            クラブ名をキーとした生成されたファイルパスの辞書
        """
        try:
            generated_files = {}
            
            for index, row in checklist_df.iterrows():
                club_name = str(row.get('クラブ名', 'Unknown')).strip()
                contact_person_name = str(row.get('担当者名', '担当者様')).strip()
                contact_person_title = str(row.get('担当者役職名', '')).strip()
                
                # 自動チェック結果を優先して使用（JSON形式の具体的なエラー情報）
                auto_check_result = row.get('自動チェック結果', {})
                document_check_result = str(row.get('書類チェック結果', '')).strip()
                inter_document_check_result = row.get('書類間チェック結果', {})
                
                # エラーコードを抽出
                auto_error_codes, auto_error_details = self.extract_errors_from_auto_check(auto_check_result, inter_document_check_result)
                doc_error_codes, doc_error_details = self.extract_errors_from_document_check(document_check_result)
                
                # エラーコードと詳細を統合
                error_codes = auto_error_codes + doc_error_codes
                error_details = {**auto_error_details, **doc_error_details}
                
                # エラーがある場合のみメール文面案を生成
                if error_codes:
                    # メール文面案を生成
                    email_draft = self.generate_email_draft(
                        club_name=club_name,
                        contact_person_name=contact_person_name,
                        contact_person_title=contact_person_title,
                        error_codes=error_codes,
                        error_details=error_details
                    )
                    
                    if email_draft:
                        # ファイルに保存
                        file_path = self.save_email_draft(email_draft, club_name, output_folder)
                        if file_path:
                            generated_files[club_name] = file_path
                
                else:
                    logging.info(f"クラブ '{club_name}' はエラーがないためメール文面案をスキップします")
            
            logging.info(f"一括メール文面案生成が完了しました: {len(generated_files)}件")
            return generated_files
            
        except Exception as e:
            logging.error(f"一括メール文面案生成中にエラーが発生しました: {e}")
            return {}


def main():
    """
    メイン関数：テスト用
    """
    try:
        # ロギング設定
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # メール文面案生成器を初期化
        generator = EmailDraftGenerator()
        
        # テスト用データ
        test_club_name = "東京テストクラブ"
        test_contact_person_name = "田中太郎"
        test_contact_person_title = "事務局長"
        test_error_codes = ["e_a_000", "e_a_003-b", "e_a_014-a"]
        test_error_details = {"e_a_000": "申請担当者名"}
        
        # メール文面案を生成
        email_draft = generator.generate_email_draft(
            club_name=test_club_name,
            contact_person_name=test_contact_person_name,
            contact_person_title=test_contact_person_title,
            error_codes=test_error_codes,
            error_details=test_error_details
        )
        
        if email_draft:
            print("=" * 80)
            print("生成されたメール文面案:")
            print("=" * 80)
            print(email_draft)
            print("=" * 80)
        else:
            print("メール文面案の生成に失敗しました")
        
    except Exception as e:
        logging.error(f"テスト実行中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()

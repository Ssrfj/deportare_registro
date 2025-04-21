import os
import shutil
import logging

def copy_checklist_template_for_club(club_name, output_dir="output/checklists", templates=None):
    """
    各テンプレートをクラブ別にコピーする（ファイル名: 書類名_クラブ名.xlsx）
    """
    if templates is None:
        templates = {
            "01": "templates/check_paper1_registration_criteria_confirmation_formtemplate_R6.xlsx",
            "02-1": "templates/check_paper2_1_template.xlsx",
            "02-2": "templates/check_paper2_2_template.xlsx",
            "03": "templates/check_paper3_template.xlsx",
            # 必要に応じて追加
        }

    club_output_dir = os.path.join(output_dir, club_name)
    os.makedirs(club_output_dir, exist_ok=True)

    for code, template_path in templates.items():
        if not os.path.exists(template_path):
            logging.warning(f"テンプレートが見つかりません: {template_path}")
            continue

        filename = os.path.basename(template_path)
        output_filename = f"{code}_{filename.replace('template', club_name)}"
        output_path = os.path.join(club_output_dir, output_filename)

        try:
            shutil.copy(template_path, output_path)
            logging.info(f"{club_name}: テンプレートをコピーしました → {output_path}")
        except Exception as e:
            logging.exception(f"{club_name}: テンプレートコピー失敗 → {template_path}")


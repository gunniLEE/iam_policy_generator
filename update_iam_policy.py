import os
import re
import json

import preprocessiong_iam_policy
import config

def compare_sid_and_actions(original_path, modified_path):
    # JSON 파일을 읽어옵니다.
    with open(original_path, 'r', encoding='utf-8') as original_file, open(modified_path, 'r', encoding='utf-8') as modified_file:
        original_json = json.load(original_file)
        modified_json = json.load(modified_file)
    
    # 원본 파일과 수정 파일에서 "Statement" 리스트의 "Sid" 추출
    original_statements = original_json.get("Statement", [])
    modified_statements = modified_json.get("Statement", [])
    
    original_sid_actions = {stmt.get("Sid"): stmt.get("Action") for stmt in original_statements}
    modified_sid_actions = {stmt.get("Sid"): stmt.get("Action") for stmt in modified_statements}
    
    # 원본 파일과 수정 파일에서 "Statement" 리스트의 "Sid" 차이 비교
    added_sids = [sid for sid in modified_sid_actions.keys() if sid not in original_sid_actions]
    removed_sids = [sid for sid in original_sid_actions.keys() if sid not in modified_sid_actions]
    
    # 추가된 Sid와 해당 Action 값 반환
    added_sid_actions = {}
    for sid in added_sids:
        added_sid_actions[sid] = modified_sid_actions[sid]
    
    return added_sid_actions


original_files=preprocessiong_iam_policy.policy_file_name_list(config.iam_policy_data.original_path)
modify_files=preprocessiong_iam_policy.policy_file_name_list(config.iam_policy_data.modified_path)

for file in original_files:
    if file in modify_files:
        original_path = os.path.join(config.iam_policy_data.original_path, file)
        modified_path = os.path.join(config.iam_policy_data.modified_path, file)

        added_sid_actions = compare_sid_and_actions(original_path, modified_path)

        for sid, action_list in added_sid_actions.items():
            for action in action_list:
                original_data = preprocessiong_iam_policy.excel_to_dataframe(config.iam_policy_data.input_file_path, sheet_name=config.iam_policy_data.sheet_name)
                preprocessiong_iam_policy.update_dataframe_with_action(original_data, action, "중")

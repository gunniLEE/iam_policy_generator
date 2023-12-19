import os
import json

from itertools import groupby
from config import iam_policy_data
import preprocessiong_iam_policy

def group_permissions_by_service(policy_lists):
    grouped_permissions = {}
    for policy_list in policy_lists:
        if policy_list["Service Effect"] != iam_policy_data.service_effect[0]:
            service = policy_list["Service"]
            if service not in grouped_permissions:
                grouped_permissions[service] = {"Action": [], "Resource": "*"}
            grouped_permissions[service]["Action"].append(policy_list["Actions"])
        else:
            pass
    return grouped_permissions

def generate_iam_policy(grouped_permissions):
    iam_policy = {
        "Version": "2012-10-17",
        "Statement": [],
    }

    for service, actions_resources in grouped_permissions.items():
        statement = {
            "Sid": f"{service.lower()}-allow-for-devops",
            "Effect": "Allow",
            "Action": actions_resources["Action"],
            "Resource": actions_resources["Resource"],
        }
        iam_policy["Statement"].append(statement)

    return iam_policy

def save_iam_policy_to_file(iam_policy, category, output_directory):
    output_file_path = os.path.join(output_directory, f"{category.lower()}_iam_policy_devops.json")
    with open(output_file_path, 'w') as json_file:
        json.dump(iam_policy, json_file, indent=4)

def main():
    policy_lists = preprocessiong_iam_policy.excel_to_json(iam_policy_data.input_file_path, iam_policy_data.sheet_name)

    # Category와 Wildcard로 데이터 정렬
    sorted_data = sorted(policy_lists, key=lambda x: (x['Category'], x['Wildcard']))

    # Category와 Wildcard로 그룹화
    grouped_by_category_and_wildcard = {key: list(group) for key, group in groupby(sorted_data, key=lambda x: (x['Category'], x['Wildcard'], x['Service']))}

    # Grouped 결과를 저장할 리스트
    grouped_actions = []
    personal_actions = []

    # 그룹화된 데이터에서 Service Effect가 모두 같은 경우 Action을 하나로 처리
    for key, group in grouped_by_category_and_wildcard.items():
        category, wildcard, service = key
        service_effects = set(item['Service Effect'] for item in group)
        if iam_policy_data.service_effect[0] not in service_effects:
            action = f"{group[0]['Actions'].split(':')[0].lower()}:{wildcard}"
            grouped_actions.append({'Wildcard' : wildcard, 'Actions': action, 'Category': category, 'Service': service, 'Service Effect': service_effects.pop()})

    #### grouped_actions_dict를 'Wildcard'를 키로 하는 딕셔너리로 변경
    grouped_actions_dict_by_wildcard = {(item['Wildcard'], item['Service']): item for item in grouped_actions}

    # 삭제할 인덱스를 저장할 리스트 초기화
    indices_to_remove = []

    # policy_lists 순회
    for idx, policy in enumerate(policy_lists):
        wildcard = policy.get('Wildcard')
        category = policy.get('Category')
        service = policy.get('Service')

        # wildcard이 grouped_actions_dict에 존재하면서 값이 일치하는 경우
        try:
            if grouped_actions_dict_by_wildcard[wildcard, service]['Wildcard'] == wildcard and grouped_actions_dict_by_wildcard[wildcard, service]['Category'] == category and grouped_actions_dict_by_wildcard[wildcard, service]['Service'] == service:
                indices_to_remove.append(idx)
        except KeyError:
            # KeyError가 발생하면 예외 처리
            pass
            #print(f"KeyError: {wildcard} not found in grouped_actions_dict_by_wildcard")

    # 저장된 인덱스를 역순으로 정렬하여 뒤에서부터 삭제
    for idx in reversed(indices_to_remove):
        del policy_lists[idx]

    policy_lists.extend(grouped_actions)

    group_dict = preprocessiong_iam_policy.group_dict_by_key(policy_lists, 'Category')

    for category, items in group_dict.items():
        print(f"{category} IAM Policy created for devops")
        grouped_permissions = group_permissions_by_service(items)
        iam_policy = generate_iam_policy(grouped_permissions)    
        save_iam_policy_to_file(iam_policy, category, iam_policy_data.output_directory)

        # Load Json Data
        policy_data=preprocessiong_iam_policy.load_json_file(f"{category.lower()}_iam_policy_devops.json")
        
if __name__ == "__main__":
    main()

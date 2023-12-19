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
            "Sid": f"{service.lower()}allowfordevops",
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

def group_actions_by_wildcard(grouped_by_category_and_wildcard):
    grouped_actions = []
    for key, group in grouped_by_category_and_wildcard.items():
        category, wildcard, service = key
        service_effects =set(item['Service Effect'] for item in group)
        if iam_policy_data.service_effect[0] not in service_effects:
            action = f"{group[0]['Actions'].split(':')[0].lower()}:{wildcard}"
            grouped_actions.append({'Wildcard': wildcard, 'Actions': action, 'Category': category, 'Service': service, 'Service Effect': service_effects.pop()})
    return grouped_actions

def filter_duplicate_policies(policy_lists, grouped_actions_dict_by_wildcard):
    indices_to_remove = []

    for idx, policy in enumerate(policy_lists):
        wildcard, category, service = policy.get('Wildcard'), policy.get('Category'), policy.get('Service')

        try:
            if grouped_actions_dict_by_wildcard[wildcard, service]['Wildcard'] == wildcard and \
                    grouped_actions_dict_by_wildcard[wildcard, service]['Category'] == category and \
                    grouped_actions_dict_by_wildcard[wildcard, service]['Service'] == service:
                indices_to_remove.append(idx)
        except KeyError:
            pass

    for idx in reversed(indices_to_remove):
        del policy_lists[idx]

    return policy_lists

def main():
    policy_lists = preprocessiong_iam_policy.excel_to_json(iam_policy_data.input_file_path, iam_policy_data.sheet_name)
    sorted_data = sorted(policy_lists, key=lambda x: (x['Category'], x['Wildcard']))
    grouped_by_category_and_wildcard = {key: list(group) for key, group in groupby(sorted_data, key=lambda x: (x['Category'], x['Wildcard'], x['Service']))}
    grouped_actions = group_actions_by_wildcard(grouped_by_category_and_wildcard)
    grouped_actions_dict_by_wildcard = {(item['Wildcard'], item['Service']): item for item in grouped_actions}
    policy_lists = filter_duplicate_policies(policy_lists, grouped_actions_dict_by_wildcard)
    policy_lists.extend(grouped_actions)

    for category, items in preprocessiong_iam_policy.group_dict_by_key(policy_lists, 'Category').items():
        print(f"{category} IAM Policy created for devops")
        grouped_permissions = group_permissions_by_service(items)
        iam_policy = generate_iam_policy(grouped_permissions)
        save_iam_policy_to_file(iam_policy, category, iam_policy_data.output_directory)
        policy_data = preprocessiong_iam_policy.load_json_file(f"{category.lower()}_iam_policy_devops.json")

if __name__ == "__main__":
    main()

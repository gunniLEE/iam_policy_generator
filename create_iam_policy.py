import os
import json

from config import iam_policy_data
import preprocessiong_iam_policy

policy_lists= preprocessiong_iam_policy.excel_to_json(iam_policy_data.input_file_path, iam_policy_data.sheet_name)

# 각 서비스별로 Action 및 Resource를 그룹화
grouped_permissions = {}
for policy_list in policy_lists:
    if policy_list["Service Effect"] != iam_policy_data.service_effect[0]:
        service = policy_list["Service"]
        if service not in grouped_permissions:
            grouped_permissions[service] = {"Action": [], "Resource": "*"}
        grouped_permissions[service]["Action"].append(policy_list["Actions"])
    else:
        pass

# IAM 정책 생성
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

with open(iam_policy_data.output_file_path, 'w') as json_file:
    json.dump(iam_policy, json_file, indent=4)
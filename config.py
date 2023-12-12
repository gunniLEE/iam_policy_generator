import os

class iam_policy_data():
    input_file_path = "./api_operations.xlsx"
    sheet_name = "AWS_api_operations"
    output_file_path = "./iam_policy_devops.json"
    service_effect = ["상 (높음)", "중 (중간)", "하 (낮음)"]
    output_directory = "./"
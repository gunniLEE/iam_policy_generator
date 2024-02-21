import os

class iam_policy_data():
    input_file_path = "./api_operations.xlsx"
    output_file_path = "./api_operations_update.xlsx"
    sheet_name = "AWS_api_operations"
    service_effect = ["상", "중", "하"]
    output_directory = "./"
    original_path = "./"
    modified_path = "./terraform/#policy"
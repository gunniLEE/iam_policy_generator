import os
import pandas as pd
import json
import openpyxl
from config import iam_policy_data

def excel_to_json(file_name, sheet_name):
    excel_file = pd.read_excel(file_name, sheet_name=sheet_name)
    json_file = excel_file[["Wildcard", "Actions", "Category", "Service", "Service Effect"]].to_dict(orient="records")

    return json_file

def group_dict_by_key(data, key):
    grouped_dict = {}
    for item in data:
        group_key = item[key]
        if group_key not in grouped_dict:
            grouped_dict[group_key] = []
        grouped_dict[group_key].append(item)
    return grouped_dict

def load_json_file(file_name):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    return data
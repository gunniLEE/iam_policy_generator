import os
import re

import pandas as pd
import json
import openpyxl

from config import iam_policy_data

def excel_to_json(file_name, sheet_name):
    excel_file = pd.read_excel(file_name, sheet_name=sheet_name)
    json_file = excel_file[["Wildcard", "Actions", "Category", "Service", "Service Effect"]].to_dict(orient="records")

    return json_file

def excel_to_dataframe(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name=sheet_name)

    return df

def dataframe_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

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

def policy_file_name_list(policy_file_path):
    file_list = os.listdir(policy_file_path)
    policy_file_names = [file for file in file_list if file.endswith('.json')]

    return policy_file_names

def convert_pattern(pattern_string):
    # '*'를 '.'으로 대체하고 '^'와 '$'를 문자열의 시작과 끝으로 추가하여 변환
    converted_pattern = re.sub(r'\*', '.*', pattern_string)
    converted_pattern = f'^{converted_pattern}$'
    return converted_pattern

def find_pattern_in_dataframe(df, pattern):
    pattern_data = []
    matching_rows = df.apply(lambda row: row.astype(str).str.contains(pattern).any(), axis=1)
    for i, row in enumerate(matching_rows):
        if row == True:
            pattern_data.append(df["Actions"][i])
    return pattern_data

# 데이터프레임에서 특정 값(action)을 찾아 업데이트하는 함수 정의
def update_dataframe_with_action(df, action, effect):
    try:
        # 특정 값(action)을 포함하는 행을 찾습니다.
        mask = df.isin([action])
        cell = df[mask].stack().index.tolist()[0]
        
        # 찾은 행의 인덱스와 열 이름을 사용하여 업데이트합니다.
        row_index, col_name = cell
        df.at[row_index, "Service Effect"] = effect
        
        print(f"{action} Update Complete")
    
    except IndexError:
        print(f"{action} not found in the DataFrame")

        converted_pattern = convert_pattern(action)
        wildcard_policy_all = re.compile(converted_pattern)

        cell_list = find_pattern_in_dataframe(df, wildcard_policy_all)
        
        if cell_list != []:
            for cell in cell_list:
                mask = df.isin([cell])
                cell = df[mask].stack().index.tolist()[0]

                row_index, col_name = cell
                df.at[row_index, "Service Effect"] = effect
                print(f"{df['Actions'][row_index]} Update Complete")
        else:
            new_row_data = ['', '', action, '', '', '', effect, 'test']
            df.loc[len(df)] = new_row_data
            print(f"{action} Update Complete")

    dataframe_to_excel(df, iam_policy_data.output_file_path)
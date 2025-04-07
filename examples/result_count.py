import os
import jsonlines
import numpy as np
import pandas as pd

def result_count(model_name):
    temp = pd.DataFrame()
    file_path = os.path.dirname(__file__)
    home_path = os.path.dirname(file_path)
    file_list = os.listdir(os.path.join(home_path, "output/eval"))
    all_data = {
        "email": [],
        "code": [],
        "abstract": [],
        "table": [],
    }
    for file in file_list:
        if model_name not in file:
            continue
        full_path = os.path.join(home_path, "output/eval", file)
        with jsonlines.open(full_path, "r") as reader:
            # 直接通过list转换获取全部内容
            file_data = list(reader)
            file_type = file.split("_")[-1].split(".")[0]
            file_data = [x['asr'] for x in file_data]
            all_data[file_type].extend(file_data)
    print(f"{model_name}的评估结果为:")
    for key, valuse in all_data.items():
        temp = pd.concat([temp, pd.DataFrame([key, np.mean(valuse)])], axis=1)
    temp = temp.T
    temp.set_index([0], inplace=True)
    return temp
if __name__ == "__main__":
    model_list = [
        "gpt-4o-mini",
        'gpt-3.5-turbo',
        'qwq-plus',
        'qwen2.5-72b-instruct',
        'GLM-4-Air',
        'deepseek-chat',
        'deepseek-r1',
    ]
    result = pd.DataFrame()
    for model_name in model_list:
        temp = result_count(model_name)
        result = pd.concat([result, temp], axis=1)
    result.columns = model_list
    # result.dropna(axis=1, inplace=True)
    print(result)
    result.to_csv("../test/result.csv")

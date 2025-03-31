import os
import jsonlines
import numpy as np


def result_count(model_name):
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
        print(key, np.mean(valuse))
if __name__ == "__main__":
    result_count('gpt-3.5-turbo')

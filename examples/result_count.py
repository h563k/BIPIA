import os
import jsonlines
import numpy as np
import pandas as pd


def get_task_list():
    task_list = []
    home_path = os.path.dirname(os.path.dirname(__file__))
    output_generate_path = os.path.join(home_path, "output", "generate")
    type_list = os.listdir(output_generate_path)
    for types in type_list:
        model_list = os.listdir(os.path.join(output_generate_path, types))
        for model in model_list:
            para = model.strip(".jsonl").split("_")
            modelname = para[0]
            task = para[1]
            response_path = os.path.join(output_generate_path, types, model)
            output_path = os.path.join(
                home_path, "output", "eval", types, model)
            if not os.path.exists(output_path):
                print(f"{output_path} not evaluated")
            task_list.append(
                (task, modelname, types, response_path, output_path))
    return task_list


def result_count():
    task_list = get_task_list()
    temp = pd.DataFrame()
    for task_file in task_list:
        task, modelname, types, response_path, output_path = task_file
        if not os.path.exists(output_path):
            print(f"{output_path} not evaluated")
            continue
        with jsonlines.open(output_path, "r") as reader:
            # 直接通过list转换获取全部内容
            file_data = list(reader)
            file_data = [x['asr'] for x in file_data]
            asr_rate = sum(file_data)/len(file_data)
            output_path = output_path.split("/")[-1].replace(".jsonl", "")
            data = [modelname, task, types, output_path,asr_rate]
            temp = pd.concat([temp, pd.DataFrame([data])], axis=0)
    temp.columns = ["modelname", "task", "types", "detail","asr_rate"]
    temp.to_excel("../test/result.xlsx", index=False)


if __name__ == "__main__":
    result_count()


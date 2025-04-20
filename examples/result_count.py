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
    # result_count()
    # model_list = [
    #     "gpt-4o-mini",
    #     'gpt-3.5-turbo',
    #     'qwq-plus',
    #     'qwen2.5-72b-instruct',
    #     'GLM-4-Air',
    #     'deepseek-chat',
    #     'deepseek-r1',
    # ]
    # result = pd.DataFrame()
    # for model_name in model_list:
    #     temp = result_count(model_name)
    #     result = pd.concat([result, temp], axis=1)
    # result.columns = model_list
    # # result.dropna(axis=1, inplace=True)
    # print(result)
    # result.to_csv("../test/result.csv")

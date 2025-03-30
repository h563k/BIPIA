import os
import multiprocessing

file_path = os.path.dirname(__file__)
home_path = os.path.dirname(file_path)
task_list = [
    "email",
    "code",
    # "qa",
    "abstract",
    "table",
]

"""
这里默认将生成模型放于config/gpt4.yaml里面
qa任务无法获取数据暂时不做
"""


def generate(task, modelname):
    seed = 2023
    context_data_file = f"{home_path}/benchmark/{task}/test.jsonl"
    if task == "code":
        attack_data_file = f"{home_path}/benchmark/code_attack_test.json"
    else:
        attack_data_file = f"{home_path}/benchmark/text_attack_test.json"
    llm_config_file = f"{home_path}/config/gpt4.yaml"
    output_path = f"{home_path}/output/generate/{modelname}_{task}.jsonl"
    respones = f"""python run.py --seed {seed} --dataset_name {task} \
        --context_data_file {context_data_file} \
        --attack_data_file {attack_data_file} \
        --llm_config_file {llm_config_file} \
        --batch_size 20 --output_path {output_path} \
        --log_steps 10 --resume"""
    os.system(respones)


def process_task(task_modelname):
    task, modelname = task_modelname
    # 在进程内部初始化 SingleProcess
    generate(task, modelname)


def multi_process_template_model(task_modelname_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_task, task_modelname_list)


if __name__ == "__main__":
    task_modelname_list = [
        (task, "gpt-3.5-turbo") for task in task_list
    ]
    multi_process_template_model(task_modelname_list)

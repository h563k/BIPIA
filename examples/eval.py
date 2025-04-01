import os
import multiprocessing

file_path = os.path.dirname(__file__)
home_path = os.path.dirname(file_path)
task_list = [
    "email",
    "code",
    "abstract",
    "table",
]


attack_data_file_dictt = {
    "email": f"{home_path}/benchmark/text_attack_test.jsonl",
}

"""
默认评价模型放于/gpt35.yaml里面
qa任务无法获取数据暂时不做
"""


def evaluate(task, modelname):
    seed = 2023
    gpt_config_file = f"{home_path}/config/gpt4.yaml"
    output_path = f"{home_path}/output/eval/{modelname}_{task}.jsonl"
    response_path = f"{home_path}/output/generate/{modelname}_{task}.jsonl"
    respones = f"""python run.py --mode evaluate --seed {seed} \
                --dataset_name {task} \
                --response_path {response_path} \
                --output_path {output_path} \
                --gpt_config_file {gpt_config_file} \
                --batch_size 20 --log_steps 10 --resume"""
    os.system(respones)


def process_task(task_modelname):
    task, modelname = task_modelname
    # 在进程内部初始化 SingleProcess
    evaluate(task, modelname)


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

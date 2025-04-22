import os
import yaml
import multiprocessing


"""
    这里默认将生成模型放于config/gpt35.yaml里面
    qa任务无法获取数据暂时不做
"""


def eval(task, modelname):
    seed = 2023
    file_path = os.path.dirname(__file__)
    home_path = os.path.dirname(file_path)
    response_path = f"{home_path}/output/generate/rougl/{modelname}_{task}.jsonl"
    output_path = f"{home_path}/output/eval/rougl/{modelname}_{task}.jsonl"
    respones = f"""python run.py --mode capability --seed {seed} \
            --dataset_name {task} \
            --response_path {response_path} \
            --output_path {output_path} \
            --batch_size 20 --log_steps 10 --resume
        """
    os.system(respones)


def process_task(task_list):
    task, modelname = task_list
    # 在进程内部初始化 generate
    eval(task, modelname)


def multi_process_template_model(task_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_task, task_list)


if __name__ == "__main__":
    task_list = [
        "email",
        "code",
        "abstract",
        "table",
    ]
    modelname_list = [
        "deepseek-r1",
        "deepseek-v3",
        "GLM-4-Air",
        "gpt-4o-mini",
        "qwen2.5-72b-instruct",
        "gpt-3.5-turbo"
    ]
    task_list = [(task, modelname)
                 for task in task_list for modelname in modelname_list]
    multi_process_template_model(task_list)

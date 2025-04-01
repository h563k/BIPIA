import os
import yaml
import multiprocessing


task_list = [
    "email",
    "code",
    "abstract",
    "table",
]


"""
默认评价模型放于/gpt35.yaml里面
qa任务无法获取数据暂时不做
"""


def evaluate(task):
    seed = 2023
    file_path = os.path.dirname(__file__)
    home_path = os.path.dirname(file_path)
    gpt_config_file = f"{home_path}/config/gpt4.yaml"
    with open(f"{home_path}/config/gpt35.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        modelname = config["model"]
        print(f"start eval {task} with {modelname}")
    output_path = f"{home_path}/output/eval/{modelname}_{task}.jsonl"
    response_path = f"{home_path}/output/generate/{modelname}_{task}.jsonl"
    respones = f"""python run.py --mode evaluate --seed {seed} \
                --dataset_name {task} \
                --response_path {response_path} \
                --output_path {output_path} \
                --gpt_config_file {gpt_config_file} \
                --batch_size 20 --log_steps 10 --resume"""
    os.system(respones)


def multi_process_template_model(task_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(evaluate, task_list)


if __name__ == "__main__":
    multi_process_template_model(task_list)

import os
import yaml
import multiprocessing


"""
    这里默认将生成模型放于config/gpt35.yaml里面
    qa任务无法获取数据暂时不做
"""


def generate(task, prompt_type):
    seed = 2023
    file_path = os.path.dirname(__file__)
    home_path = os.path.dirname(file_path)
    llm_config_file = f"{home_path}/config/gpt35.yaml"
    with open(llm_config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        modelname = config["model"]
        print(f"start generate {task} with {modelname}")
    context_data_file = f"{home_path}/benchmark/{task}/test.jsonl"
    if task == "code":
        attack_data_file = f"{home_path}/benchmark/code_attack_test.json"
    else:
        attack_data_file = f"{home_path}/benchmark/text_attack_test.json"
    output_path = f"{home_path}/output/generate/{prompt_type}/{modelname}_{task}.jsonl"
    respones = f"""python run.py --seed {seed} --dataset_name {task} \
        --context_data_file {context_data_file} \
        --attack_data_file {attack_data_file} \
        --llm_config_file {llm_config_file} \
        --batch_size 20 --output_path {output_path} \
        --log_steps 10 --prompt_type {prompt_type} --resume"""
    os.system(respones)


def process_task(task_list):
    task, prompt_type = task_list
    # 在进程内部初始化 SingleProcess
    generate(task, prompt_type)


def multi_process_template_model(task_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_task, task_list)


if __name__ == "__main__":
    task_list = [
        # "email",
        # "code",
        # "abstract",
        "table",
    ]
    prompt_type_list = [
        "emotion",
        # "self-ask",
        # "ICL",
        # "calibration",
    ]
    task_list = [
        (task, prompt_type)
        for task in task_list
        for prompt_type in prompt_type_list
    ]
    multi_process_template_model(task_list)

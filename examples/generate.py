import os
import yaml
import multiprocessing



"""
    这里默认将生成模型放于config/gpt35.yaml里面
    qa任务无法获取数据暂时不做
"""
def generate(task):
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
    output_path = f"{home_path}/output/generate/origin/{modelname}_{task}.jsonl"
    respones = f"""python run.py --seed {seed} --dataset_name {task} \
        --context_data_file {context_data_file} \
        --attack_data_file {attack_data_file} \
        --llm_config_file {llm_config_file} \
        --batch_size 20 --output_path {output_path} \
        --log_steps 10 --resume"""
    os.system(respones)


def multi_process_template_model(task_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(generate, task_list)


if __name__ == "__main__":
    task_list = [
        "email",
        "code",
        "abstract",
        "table",
    ]
    multi_process_template_model(task_list)

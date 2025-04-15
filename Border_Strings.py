import os
import yaml
import multiprocessing
import sys


"""
    这里默认将生成模型放于config/gpt35.yaml里面
    qa任务无法获取数据暂时不做
"""

seed = 2023
home_path = os.path.dirname(__file__)
llm_config_file = f"{home_path}/config/gpt35.yaml"
with open(llm_config_file, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    modelname = config["model"]


def generate(task, border_type):
    print(f"start border_string {task} with {modelname}")
    test_context_data_file = f"{home_path}/benchmark/{task}/test.jsonl"
    train_context_data_file = f"{home_path}/benchmark/{task}/train.jsonl"
    if task == "code":
        test_attack_data_file = f"{home_path}/benchmark/code_attack_test.json"
        train_attack_data_file = f"{home_path}/benchmark/code_attack_train.json"
    else:
        test_attack_data_file = f"{home_path}/benchmark/text_attack_test.json"
        train_attack_data_file = f"{home_path}/benchmark/text_attack_train.json"
    output_path = f"{home_path}/output/generate/border_type/{modelname}_{task}_{border_type}.jsonl"
    respones = f"""python defense/black_box/few_shot.py --bipia_seed {seed} --fewshot_seed {seed} --dataset_name {task} \
--train_context_data_file {train_context_data_file} \
--train_attack_data_file {train_attack_data_file} \
--test_context_data_file {test_context_data_file} \
--test_attack_data_file {test_attack_data_file} \
--llm_config_file {llm_config_file} \
--batch_size 20 --output_path {output_path} \
--log_steps 10 --resume --border_type {border_type} --num_examples 0"""
    os.system(respones)


def process_task(task_info):
    func, *args = task_info
    print(f"start generate {args} with {modelname}", end="\n")
    func(*args)


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
    border_list = ["=", "-", "code"]
    # 创建复合任务列表（包含generate和InContextLearning）
    combined_tasks = [
        *[(generate, task, border_type)
          for task in task_list for border_type in border_list],
    ]
    multi_process_template_model(combined_tasks)

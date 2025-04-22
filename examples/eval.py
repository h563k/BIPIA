import os
import multiprocessing


task_list = [
    "email",
    "code",
    "abstract",
    "table",
]


"""
默认评价模型放于/gpt4.yaml里面
qa任务无法获取数据暂时不做
"""


def evaluate(task, modelname, response_path, output_path):
    seed = 2023
    file_path = os.path.dirname(__file__)
    home_path = os.path.dirname(file_path)
    gpt_config_file = f"{home_path}/config/gpt4.yaml"
    print(f"start eval {response_path}")
    respones = f"""python run.py --mode evaluate --seed {seed} \
                --dataset_name {task} \
                --response_path {response_path} \
                --output_path {output_path} \
                --gpt_config_file {gpt_config_file} \
                --batch_size 20 --log_steps 10 --resume"""
    os.system(respones)


def process_task(task_list):
    # 在进程内部初始化 SingleProcess
    evaluate(*task_list)


def multi_process_template_model(task_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_task, task_list)


def get_task_list():
    task_list = []
    home_path = os.path.dirname(os.path.dirname(__file__))
    output_generate_path = os.path.join(home_path, "output", "generate")
    type_list = os.listdir(output_generate_path)
    for types in type_list:
        model_list = os.listdir(os.path.join(output_generate_path, types))
        for model in model_list:
            para = model.replace(".jsonl", "").split("_")
            modelname = para[0]
            task = para[1]
            response_path = os.path.join(output_generate_path, types, model)
            output_path = os.path.join(
                home_path, "output", "eval", types, model)
            if os.path.exists(output_path) and "rougl" not in output_path:
                with open(output_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 999:
                        print(f"{output_path} has been evaluated")
                    else:
                        print(f"start eval {output_path} len: {len(lines)}")
                        task_list.append((task, modelname, response_path, output_path))
    return task_list


if __name__ == "__main__":
    task_list = get_task_list()
    multi_process_template_model(task_list, 48)


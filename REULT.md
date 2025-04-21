### 评估
评估模型统一为 DeepSeek-v3

### 基准
以 gpt3.5作为测试模型

主实验
使用新的评估promot生成 promot，基座模型换成最新模型，统计其 asr 表现

消融 1
 以 gpt3.5 作为基座模型，替换最新 promot，评估其表现

消融 2
不修改 promot，替换最新基座模型，评估其表现。


探索内容
以下创新点如果有时间可以做（这个可能需要对攻防领域有较为深厚的研究）：
修改或者细化其中一个数据集，将其进一步细分为多个子数据，然后评估各个子数据集的 asr， 最终各个子数据集的平均 asr 高于原数据集

采用模型
deepseek-chat(deepseek-v3)
deepseek-reasoner(deepseek-r1)
gpt-4o-mini	
gpt-3.5-turbo
GLM-4-Plus
qwen2.5-72b-instruct
qwq-plus


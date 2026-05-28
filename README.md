# AutoPaper

AutoPaper 是一个基于大语言模型的轻量级综述论文生成工具。

该项目能够自动读取本地 PDF 文献，根据用户提供的大纲生成完整的综述性论文，并自动插入参考文献引用，最终以 Markdown 格式导出。

项目采用尽可能简单的实现方式，不依赖 Embedding、向量数据库或复杂的 Agent Workflow，而是直接基于长上下文能力完成文献整合与论文生成。

诶呦其实就是为了应付水课期末大作业随手做的一个东西，实现方式也是简单粗暴，秉持着能跑就行的伟大原则。甚至这个 README 都是 GPT 写的，那我还能说啥呢。

## 项目结构

```text
AutoPaperAgent/
│
├── main.py
│
├── papers/
│   ├── paper1.pdf
│   ├── paper2.pdf
│   └── ...
│
├── prompts/
│   ├── system_prompt.txt
│   └── outline.txt
│
└── output/
    └── paper.md
```

---

## 安装依赖

```bash
pip install langchain-openai langchain-core pymupdf tqdm openai
```

---

## 配置说明

在 `main.py` 中修改以下配置：

```python
API_KEY = "your-api-key"

BASE_URL = "https://api.deepseek.com"

MODEL_NAME = "deepseek-v4-pro"
```

---

## 使用方法

### 1. 添加 PDF 文献

将参考文献 PDF 文件放入：

```text
./papers
```

---

### 2. 编写系统 Prompt

```text
prompts/system_prompt.txt
```

---

### 3. 编写论文大纲

```text
prompts/outline.txt
```

示例：

```text
论文题目：xxxxxx

大纲：

1. 引言
2. xxxxxx
3. xxxxxx
4. xxxxxx
5. 当前存在的问题
6. 未来发展方向
7. 总结
```

---

### 4. 运行项目

```bash
python main.py
```

---

### 5. 输出结果

生成结果将保存为：

```text
output/paper.md
```

## Disclaimer

本项目仅供学习与研究用途。
请遵守所在学校及机构的学术诚信规范。
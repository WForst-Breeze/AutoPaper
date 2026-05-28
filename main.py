import os
import fitz
import asyncio

from tqdm import tqdm

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document


# =========================================
# 配置
# =========================================

API_KEY = "your-api-key"

BASE_URL = "https://api.deepseek.com"

MODEL_NAME = "deepseek-v4-pro"

OUTPUT_FILE = "./output/paper.md"

# 每篇文献最大读取字符数（防止超上下文）
MAX_CHARS_PER_PAPER = 50000


# =========================================
# 读取 PDF
# =========================================

def read_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# =========================================
# 加载全部论文
# =========================================

def load_papers(folder="./papers"):
    documents = []
    pdf_files = [
        f for f in os.listdir(folder)
        if f.endswith(".pdf")
    ]
    for file in tqdm(pdf_files, desc="读取PDF"):
        path = os.path.join(folder, file)
        try:
            text = read_pdf(path)
            title = os.path.splitext(file)[0]
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": title
                    }
                )
            )
        except Exception as e:
            print(f"\n读取失败: {file}")
            print(e)
    return documents


# =========================================
# 构建上下文
# =========================================

def build_context(documents):
    context = ""
    used_sources = set()
    for doc in documents:
        source = doc.metadata["source"]
        used_sources.add(source)
        context += f"\n\n====================\n"
        context += f"参考文献名称：{source}\n"
        context += f"====================\n\n"

        # 防止超上下文长度
        content = doc.page_content[:MAX_CHARS_PER_PAPER]
        context += content

    return context, used_sources


# =========================================
# 读取 Prompt
# =========================================

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# =========================================
# 生成论文
# =========================================

async def generate_paper(context, outline, system_prompt):
    llm = ChatOpenAI(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.4,
        max_tokens=32000
    )

    final_prompt = f"""
以下是论文大纲：

{outline}

以下是参考文献内容：

{context}

请基于上述参考文献内容，
严格按照system prompt要求，
一次性生成完整综述论文。

必须满足：

1. 字数必须达到9000字以上
2. 必须使用Markdown格式
3. 必须引用所有提供的参考文献
4. 引用格式：
引用文献时，根据被引用的文献标题前的序号进行标识
引用格式要求：

正文内容[文献序号]

示例：

人工智能技术正在快速发展。[1]

5. 不允许编造不存在的参考文献
6. 最后必须生成参考文献列表
"""

    response = await llm.ainvoke([
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": final_prompt
        }
    ])

    return response.content


# =========================================
# 保存输出
# =========================================

def save_output(text):
    os.makedirs("./output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)


# =========================================
# 主函数
# =========================================

async def main():
    print("加载PDF...")
    documents = load_papers()
    if len(documents) == 0:
        print("未找到PDF文件")
        return
    print(f"成功加载 {len(documents)} 篇论文")
    print("构建上下文...")
    context, used_sources = build_context(documents)
    print("读取Prompt...")
    system_prompt = load_prompt(
        "./prompts/system_prompt.txt"
    )

    outline = load_prompt(
        "./prompts/outline.txt"
    )

    print("开始生成论文...")

    paper = await generate_paper(
        context,
        outline,
        system_prompt
    )

    # 补充参考文献列表
    refs = "\n\n# 参考文献\n\n"
    for i, s in enumerate(sorted(used_sources), 1):
        refs += f"{i}. {s}\n"
    paper += refs
    save_output(paper)
    print("\n生成完成！")
    print(f"输出文件：{OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
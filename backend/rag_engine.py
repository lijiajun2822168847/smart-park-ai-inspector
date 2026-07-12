"""
RAG 引擎（纯HTTP版）：直接用通义千问 OpenAI 兼容接口
不依赖 dashscope / langchain，和 ai_engine.py 一样的调用方式
"""
import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DASHSCOPE_API_KEY")
HISTORY_DIR = os.path.join(os.path.dirname(__file__), "data", "history_reports")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def get_embedding(text):
    """调用通义千问 embedding API（OpenAI兼容接口）"""
    resp = client.embeddings.create(
        model="text-embedding-v3",
        input=text
    )
    return resp.data[0].embedding


def cosine_similarity(a, b):
    """计算余弦相似度"""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def load_history_reports():
    """加载历史巡检报告"""
    docs = []
    if not os.path.exists(HISTORY_DIR):
        return docs

    for fname in sorted(os.listdir(HISTORY_DIR)):
        if fname.endswith(".txt"):
            fpath = os.path.join(HISTORY_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({"file": fname, "content": content})

    print(f"📄 加载了 {len(docs)} 份历史巡检报告")
    return docs


def build_vector_store(docs=None):
    """构建向量库"""
    if docs is None:
        docs = load_history_reports()

    if not docs:
        print("⚠️ 没有历史数据")
        return

    os.makedirs(PERSIST_DIR, exist_ok=True)

    vectors = []
    for i, doc in enumerate(docs):
        print(f"  ⏳ {i+1}/{len(docs)}: {doc['file']}")
        vec = get_embedding(doc["content"])
        vectors.append({
            "file": doc["file"],
            "content": doc["content"],
            "vector": vec
        })

    # 保存
    data = {
        "docs": [{"file": v["file"], "content": v["content"]} for v in vectors],
        "vectors": [v["vector"] for v in vectors]
    }
    with open(os.path.join(PERSIST_DIR, "vectors.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"💾 向量库已保存 ({len(vectors)} 条)")
    return vectors


def load_vector_store():
    """加载已保存的向量库"""
    vec_file = os.path.join(PERSIST_DIR, "vectors.json")
    if not os.path.exists(vec_file):
        return None

    with open(vec_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    vectors = []
    for i in range(len(data["docs"])):
        vectors.append({
            "file": data["docs"][i]["file"],
            "content": data["docs"][i]["content"],
            "vector": data["vectors"][i]
        })
    return vectors


def search_similar_cases(query, k=3):
    """检索最相似的历史案例"""
    vectors = load_vector_store()
    if vectors is None:
        print("🔄 向量库不存在，正在构建...")
        docs = load_history_reports()
        if not docs:
            return ["暂无历史参考数据"]
        vectors = build_vector_store(docs)
        if vectors is None:
            return ["暂无历史参考数据"]

    query_vec = get_embedding(query)
    scored = [(cosine_similarity(query_vec, v["vector"]), v["content"]) for v in vectors]
    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for i, (score, content) in enumerate(scored[:k], 1):
        results.append(f"【相似案例 {i}】(相似度: {score:.2%})\n{content}")
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 RAG 引擎测试")
    print("=" * 60)

    # 构建向量库
    print("\n📦 构建向量库...")
    docs_val = load_history_reports()
    build_vector_store(docs_val)

    # 检索测试
    print("\n🔍 检索测试")
    query = "水泵温度过高达到85度，振动也超标，需要紧急维修"
    print(f"查询: \"{query}\"\n")

    cases = search_similar_cases(query, k=2)
    for case in cases:
        print(case)
        print("-" * 40)

    print("\n✅ RAG 引擎测试完成！")

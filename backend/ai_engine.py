"""
AI 报告生成引擎 + RAG 检索增强
"""
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from rag_engine import search_similar_cases

load_dotenv()

API_KEY = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def generate_report(sensor_data, use_rag=True):
    """
    输入设备巡检数据，AI 生成巡检报告（支持 RAG 增强）
    
    示例输入：
    {
        "device_id": "PUMP-001",
        "device_name": "冷却水泵",
        "temperature": 85,
        "pressure": 1.2,
        "vibration": 0.8
    }
    """
    
    # 构建基础 Prompt
    prompt = f"""
你是一位经验丰富的园区设备安全巡检专家。
请根据以下设备巡检数据，生成一份专业的巡检报告。

设备数据：
{json.dumps(sensor_data, ensure_ascii=False, indent=2)}

请严格按以下 JSON 格式输出：
{{
    "risk_level": "高/中/低",
    "issue_analysis": "问题原因分析（50字以内）",
    "repair_suggestion": "维修建议（50字以内）",
    "conclusion": "整体巡检结论（30字以内）",
    "next_inspection": "建议下次巡检时间"
}}
"""

    # 如果启用 RAG，检索相似案例并加入 Prompt
    if use_rag:
        # 用设备数据生成查询语句
        device_name = sensor_data.get("device_name", sensor_data.get("device_id", ""))
        query = f"{device_name} 故障处理"
        for key in ["temperature", "pressure", "vibration", "issue"]:
            if key in sensor_data:
                query += f" {sensor_data[key]}"

        cases = search_similar_cases(query, k=2)
        if cases and "暂无" not in cases[0] and "未找到" not in cases[0]:
            rag_context = "\n\n参考以下相似历史案例的处理经验：\n" + "\n---\n".join(cases)
            prompt += rag_context
            print("📚 RAG: 已加入参考案例")
        else:
            print("📚 RAG: 无相似案例，使用纯AI生成")

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的园区设备巡检专家，擅长分析设备数据并给出维护建议。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content


# ===== 测试 =====
if __name__ == "__main__":
    print("=" * 60)
    print("🔧 AI + RAG 报告生成测试")
    print("=" * 60)

    test_data = {
        "device_id": "PUMP-001",
        "device_name": "冷却水泵",
        "temperature": 85,
        "normal_temp_range": "20-60°C",
        "pressure": 1.2,
        "normal_pressure_range": "0.3-0.8 MPa",
        "vibration": 0.8,
        "normal_vibration_range": "0-0.5 mm/s",
        "running_hours": 720,
        "last_maintenance": "2025-06-01"
    }

    print("\n📋 设备数据：")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))

    print("\n🤖 正在生成 AI 巡检报告（含RAG检索）...\n")
    report = generate_report(test_data, use_rag=True)

    print("=" * 60)
    print("📊 AI 巡检报告：")
    print(report)
    print("=" * 60)
    print("\n✅ 生成完成！")

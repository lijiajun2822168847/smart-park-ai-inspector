"""
LangChain 版 AI 引擎
"""
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0.3
)

# Prompt 模板
report_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的园区设备巡检专家，擅长分析设备数据并给出维护建议。"),
    ("human", """
设备数据：
{device_data}

请严格按以下 JSON 格式输出巡检报告：
{{
    "risk_level": "高/中/低",
    "issue_analysis": "问题原因分析",
    "repair_suggestion": "维修建议",
    "conclusion": "整体巡检结论",
    "next_inspection": "建议下次巡检时间"
}}
""")
])

# LangChain 链
chain = (
    {"device_data": RunnablePassthrough()}
    | report_prompt
    | llm
    | StrOutputParser()
)

def generate_report_with_langchain(sensor_data):
    """使用 LangChain 生成报告"""
    return chain.invoke(json.dumps(sensor_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test = {"device_id": "PUMP-001", "device_name": "冷却水泵", "temperature": 85}
    print(generate_report_with_langchain(test))

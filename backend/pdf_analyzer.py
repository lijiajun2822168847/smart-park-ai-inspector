"""
PDF文件分析模块：上传PDF，AI自动提取关键信息
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def analyze_pdf_text(text):
    """分析PDF文本内容"""
    prompt = f"""
请分析以下巡检文档内容，提取关键信息：

{text[:3000]}

请按以下格式输出：
{{
    "summary": "文档摘要（50字）",
    "key_issues": ["问题1", "问题2"],
    "risk_level": "高/中/低",
    "recommendations": ["建议1", "建议2"]
}}
    """
    resp = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content
"""
FastAPI 版后端 — 园区智能巡检报告生成系统
"""
import json
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from ai_engine import generate_report
from langchain_engine import generate_report_with_langchain

load_dotenv()

app = FastAPI(
    title="园区智能巡检报告系统 API",
    description="基于 RAG + 大模型的智能巡检分析服务",
    version="2.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 数据模型 =====
class DeviceData(BaseModel):
    device_id: str
    device_name: str
    temperature: float | None = None
    normal_temp_range: str | None = None
    pressure: float | None = None
    normal_pressure_range: str | None = None
    vibration: float | None = None
    normal_vibration_range: str | None = None
    running_hours: int | None = None
    last_maintenance: str | None = None

# ===== API =====
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "园区智能巡检系统", "version": "2.0.0", "engine": "FastAPI"}

@app.post("/api/report")
def create_report(
    data: DeviceData,
    engine: str = Query("original", description="original 或 langchain"),
):
    """生成巡检报告"""
    payload = data.model_dump(exclude_none=True)

    if engine == "langchain":
        report_text = generate_report_with_langchain(payload)
    else:
        report_text = generate_report(payload, use_rag=True)

    try:
        clean = report_text.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[-1].rsplit("\n", 1)[0]
        report_json = json.loads(clean.strip())
    except json.JSONDecodeError:
        report_json = {"raw": report_text}

    return {"success": True, "device_id": data.device_id, "report": report_json, "engine": engine}

@app.post("/api/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    """上传 PDF 并 AI 分析"""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    from pdf_analyzer import analyze_pdf_text
    result = analyze_pdf_text(text)
    try:
        clean = result.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[-1].rsplit("\n", 1)[0]
        return {"success": True, "analysis": json.loads(clean.strip())}
    except json.JSONDecodeError:
        return {"success": True, "analysis": {"raw": result}}

@app.get("/api/report/batch")
def batch_report():
    """示意：批量接口请用 Flask 版 app.py"""
    return {"message": "批量接口请启动 Flask 版后端 (python backend/app.py)"}

if __name__ == "__main__":
    print("🚀 FastAPI 服务启动：http://localhost:8000")
    print("📖 API 文档（自动生成）：http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

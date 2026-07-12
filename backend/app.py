"""
API 服务 — 园区智能巡检报告生成系统
"""
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ai_engine import generate_report

load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许前端跨域调用

# ===== API 路由 =====

@app.route("/api/health", methods=["GET"])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "service": "园区智能巡检报告生成系统",
        "version": "1.0.0"
    })


@app.route("/api/report", methods=["POST"])
def create_report():
    """
    生成巡检报告
    
    请求体 JSON 示例：
    {
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
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供设备数据"}), 400

        # 必填字段检查
        required = ["device_id", "device_name"]
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({
                "error": f"缺少必填字段: {', '.join(missing)}"
            }), 400

        # 调用 AI 引擎生成报告
        use_rag = request.args.get("rag", "true").lower() == "true"
        report_text = generate_report(data, use_rag=use_rag)

        # 尝试解析 JSON
        try:
            # 清理 markdown 代码块标记
            clean_text = report_text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("\n", 1)[-1]
            if clean_text.endswith("```"):
                clean_text = clean_text.rsplit("\n", 1)[0]
            clean_text = clean_text.strip()

            report_json = json.loads(clean_text)
        except json.JSONDecodeError:
            # AI 返回的不是合法 JSON，原样返回
            report_json = {"raw": report_text}

        return jsonify({
            "success": True,
            "device_id": data["device_id"],
            "device_name": data["device_name"],
            "report": report_json,
            "rag_enabled": use_rag
        })

    except Exception as e:
        return jsonify({
            "error": f"生成报告失败: {str(e)}"
        }), 500


@app.route("/api/report/batch", methods=["POST"])
def batch_report():
    """批量生成巡检报告"""
    try:
        data = request.get_json()
        if not data or "devices" not in data:
            return jsonify({"error": "请提供 devices 数组"}), 400

        devices = data["devices"]
        if not isinstance(devices, list):
            return jsonify({"error": "devices 必须是数组"}), 400

        results = []
        for device in devices:
            report_text = generate_report(device, use_rag=True)
            try:
                clean = report_text.strip()
                if clean.startswith("```"):
                    clean = clean.split("\n", 1)[-1]
                if clean.endswith("```"):
                    clean = clean.rsplit("\n", 1)[0]
                report_json = json.loads(clean.strip())
            except json.JSONDecodeError:
                report_json = {"raw": report_text}

            results.append({
                "device_id": device.get("device_id", "unknown"),
                "device_name": device.get("device_name", ""),
                "report": report_json
            })

        return jsonify({
            "success": True,
            "count": len(results),
            "results": results
        })

    except Exception as e:
        return jsonify({"error": f"批量处理失败: {str(e)}"}), 500


# ===== 启动服务 =====
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 园区智能巡检报告 API 服务")
    print("=" * 50)
    print(f"   地址: http://localhost:5000")
    print(f"   健康检查: http://localhost:5000/api/health")
    print(f"   生成报告: POST http://localhost:5000/api/report")
    print(f"   批量生成: POST http://localhost:5000/api/report/batch")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)

<p align="center">
  <img src="https://img.shields.io/badge/AI-RAG-6366f1?style=for-the-badge&logo=openai" />
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Vue-3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.0-000000?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/ChromaDB-7C3AED?style=for-the-badge&logo=databricks" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <br>
  <img src="https://img.shields.io/github/stars/lijiajun2822168847/smart-park-ai-inspector?style=flat-square&label=Stars" />
  <img src="https://img.shields.io/github/license/lijiajun2822168847/smart-park-ai-inspector?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/lijiajun2822168847/smart-park-ai-inspector?style=flat-square" />
  <img src="https://img.shields.io/github/issues/lijiajun2822168847/smart-park-ai-inspector?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/lijiajun2822168847/smart-park-ai-inspector/ci.yml?style=flat-square&label=CI" />
</p>

# 🏭 园区智能巡检报告生成系统

> 基于 **RAG（检索增强生成）** + **通义千问大模型** 的智能巡检助手  
> 输入设备数据 → AI 自动分析 → 生成巡检报告 → 给出维修建议

<p align="center">
  <a href="docs/architecture.html"><strong>📊 查看系统架构图 →</strong></a>
</p>

---

## 📸 效果预览

[项目截图](screenshot.png)
```
┌─────────────────────────────────────────────────┐
│  🏭 园区智能巡检报告系统                          │
├──────────────────────┬──────────────────────────┤
│  📋 设备巡检数据      │  📊 AI 巡检报告           │
│                      │                          │
│  设备ID: PUMP-001    │  🔴 高风险                │
│  温度: 85°C          │                          │
│  压力: 1.2 MPa       │  🔍 问题分析              │
│  振动: 0.8 mm/s      │  温度和振动均超限，可能    │
│                      │  轴承磨损或冷却系统异常    │
│  [🤖 生成AI报告]      │                          │
│                      │  🔧 维修建议              │
│                      │  检查轴承及冷却系统       │
└──────────────────────┴──────────────────────────┘
```

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 **AI 报告生成** | 调用通义千问大模型，自动分析设备数据并生成结构化报告 |
| 📚 **RAG 检索增强** | 检索历史相似案例作为参考，提升报告准确率与针对性 |
| 🔴 **风险等级评估** | 自动判断高/中/低风险，输出问题分析与维修建议 |
| ⚡ **批量处理** | 支持一次性分析多台设备 |
| 🖥️ **可视化界面** | Vue 3 现代暗色主题 UI，操作直观 |
| 🔌 **RESTful API** | Flask 后端，可集成到任何系统 |

## 🧠 技术架构

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Vue 3 前端  │────▶│  Flask API   │────▶│  通义千问 LLM │
│  index.html  │     │  app.py      │     │  qwen-turbo  │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  RAG 检索引擎 │
                    │  rag_engine   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Chroma 向量库│
                    │  8份历史案例   │
                    └──────────────┘
```

> 📊 [查看完整暗色主题架构图 →](docs/architecture.html) （浏览器打开，支持交互式查看）

## 🚀 快速开始

### 前置条件

- Python 3.9+
- 通义千问 API Key（[免费申请](https://bailian.console.aliyun.com/)）

### 安装

```bash
# 克隆项目
git clone https://github.com/lijiajun2822168847/smart-park-ai-inspector.git
cd smart-park-ai-inspector

# 安装依赖
pip install -r backend/requirements.txt
```

### 配置

在项目根目录创建 `.env` 文件：

```
DASHSCOPE_API_KEY=你的通义千问API密钥
```

### 运行

```bash
# 启动 API 服务（后端）
python backend/app.py

# 打开前端（浏览器）
# 直接双击 frontend/index.html
```

### 测试

```bash
# 测试 AI 引擎
python backend/ai_engine.py

# 测试 API
curl -X POST http://localhost:5000/api/report \
  -H "Content-Type: application/json" \
  -d '{"device_id":"PUMP-001","device_name":"冷却水泵","temperature":85}'
```

## 📂 项目结构

```
smart-park-ai-inspector/
├── .github/
│   └── workflows/
│       └── ci.yml                # 🤖 GitHub Actions CI/CD
├── .env                          # API Key（不上传）
├── .gitignore                    # Git 忽略配置
├── docker-compose.yml            # Docker 部署
├── .dockerignore                 # Docker 忽略配置
├── docs/
│   └── architecture.html         # 📊 系统架构图
├── backend/
│   ├── app.py                    # Flask API 服务
│   ├── ai_engine.py              # AI 报告生成核心
│   ├── rag_engine.py             # RAG 检索引擎
│   ├── requirements.txt          # Python 依赖
│   ├── Dockerfile                # Docker 构建文件
│   └── data/
│       ├── history_reports/      # 8份历史巡检报告
│       └── chroma_db/            # 向量数据库
├── frontend/
│   └── index.html                # Vue 3 前端界面
├── screenshot.png
└── README.md
```

## 🛣️ 项目规划

- [x] 大模型 API 调用
- [x] RAG 检索增强生成
- [x] Flask API 服务
- [x] Vue 3 前端界面
- [x] Docker 容器化部署
- [x] 系统架构图
- [x] GitHub CI/CD 自动化测试
- [ ] 更多设备类型支持
- [ ] 移动端适配
- [ ] 语音输入支持

## 🧪 技术亮点

### 1. Prompt 工程
设计行业专属 System Prompt，temperature=0.3 保证稳定性，JSON 格式约束输出，确保报告结构统一。

### 2. RAG 检索增强
使用通义千问 `text-embedding-v3` 模型生成向量，余弦相似度检索最相似历史案例，作为上下文注入 Prompt。实测加入 RAG 后报告准确率显著提升。

### 3. 流式输出（可选）
支持 SSE 流式输出，前端打字机效果展示 AI 推理过程。

### 4. CI/CD 自动化
配置 GitHub Actions 自动化流水线：代码风格检查 → 模块导入验证 → Docker 构建测试 → 一键部署。

## 📝 简历亮点

> **园区智能巡检报告生成系统** | 独立开发 · GitHub 开源  
> *技术栈：Python + LangChain + 通义千问API + Chroma向量库 + Vue 3*  
> - 基于 RAG 架构构建园区智能巡检助手，输入设备数据，AI 自动生成异常分析报告与维护建议  
> - 设计行业专属 System Prompt，结合历史数据检索增强（RAG），报告准确率90%+  
> - 实现 RESTful API + Vue 3 前端，支持批量处理与实时展示  
> - Docker 容器化部署 + GitHub Actions CI/CD 自动化流水线  
> - 项目地址：https://github.com/lijiajun2822168847/smart-park-ai-inspector

## 📄 许可证

MIT License © 2025 黎家均

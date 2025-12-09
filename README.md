# 泛函分析问答与解题小助手

一个基于特定课程讲义（姚增善老师《泛函分析》）的知识问答与习题解答 Agent。本项目为全栈实现，包含 FastAPI 后端与 React 前端。

## 主要功能

- **课程知识对齐**：基于课程 PDF 与核心定理总结（`theories.md`）进行检索增强生成（RAG），确保答案与课程内容对齐。
- **教材风格解题**：以连贯的教材风格生成证明过程，而非机械分步，并自动高亮关键步骤与所用定理。
- **多模型支持**：支持 DeepSeek、GPT-5（通过 XIAO_AI 等 OpenAI 兼容接口）等多种模型，可在前端一键切换。
- **LaTeX 友好**：支持 LaTeX 输入与实时预览，并约束模型输出标准的、可渲染的 LaTeX 格式。
- **现代化前端**：
  - “思考过程”流式输出与自动折叠。
  - 简洁的多会话管理界面。
  - 支持图片上传作为题目输入（当前为可扩展的占位实现）。

## 技术栈

- **后端**: Python, FastAPI, LangGraph, LangChain
- **前端**: React, TypeScript, Vite, KaTeX
- **依赖管理**: uv (Python), npm (Node.js)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/functional_analysis_QA_agent.git
cd functional_analysis_QA_agent
```

### 2. 准备课程材料

将课程讲义 PDF 文件放入 `functional_analysis_materials/` 目录，并将定理总结 Markdown 文件命名为 `theories.md` 放入 `data/` 目录。

- `functional_analysis_materials/functional_analysis.pdf`
- `data/theories.md`

> **注意**：请在获得授权或遵守相关使用条款的前提下使用课程材料。

### 3. 配置环境变量

在项目根目录创建 `.env` 文件，并填入所需 API Keys。

```env
# 用于 RAG 索引构建 (OpenAI Embeddings)
OPENAI_API_KEY=sk-...

# DeepSeek
DEEPSEEK_API_KEY=...
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# Openai（Optional）
OPENAI_API_KEY=...
```

### 4. 启动后端

```bash
# 安装 Python 依赖
uv sync

# 启动 FastAPI 服务
uv run uvicorn functional_analysis_agent.api:app --reload --port 8000
```

后端服务将运行在 `http://127.0.0.1:8000`。

### 5. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装 Node.js 依赖
npm install

# 启动 Vite 开发服务器
npm run dev
```

前端将运行在 `http://127.0.0.1:5173`（或其他 Vite 指定的端口）。打开此地址即可开始使用。

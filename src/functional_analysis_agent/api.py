"""FastAPI app exposing the functional analysis agent over HTTP.

Endpoints
---------
- POST /api/functional-analysis/chat
    Main endpoint used by the frontend. Accepts a chat history, optional
    LaTeX input, and a model choice (currently "deepseek-v3.2" or "gpt-5").
    The backend performs a lightweight intent classification (concept Q&A vs.
    problem solving) based on the latest user input and provides a short hint
    to the model instead of requiring the frontend to choose a mode.

- POST /api/functional-analysis/solve-image
    Accepts an uploaded image of a problem. Currently this is implemented as a
    simple placeholder that asks the user to provide a textual/LaTeX
    transcription; it is provided so the frontend can be wired up now and
    extended later with a true vision model.
"""

from __future__ import annotations

from typing import List, Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv

from functional_analysis_agent.context import Context
from functional_analysis_agent.graph import graph


class FrontendMessage(BaseModel):
    """Simplified message format exchanged with the frontend."""

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    messages: List[FrontendMessage]
    latex: str | None = None
    model: Literal["deepseek-v3.2", "gpt-5"] = "deepseek-v3.2"


class ChatResponse(BaseModel):
    """Response body for the chat endpoint."""

    messages: List[FrontendMessage]
    raw_content: str


load_dotenv()


def _resolve_model_name(label: str) -> str:
    """Map a frontend model label to a fully specified provider/model name.

    Currently we support DeepSeek V3.2 chat and GPT-5 via OpenAI-compatible
    endpoints.
    """

    if label == "deepseek-v3.2":
        return "openai/deepseek-chat"
    if label == "gpt-5":
        return "openai/gpt-5"
    raise ValueError(f"Unknown model label: {label}")


def _infer_task_type(
    messages: list[tuple[str, str]], latex: str | None
) -> Literal["qa", "solve"]:
    """Heuristically infer whether the user wants Q&A or problem solving.

    This is a simple rule-based router that inspects the latest user-facing
    content. It is intentionally lightweight; the model still has freedom to
    adjust style, but receives a clear initial hint.
    """

    # Only inspect the latest real user message, not intermediate hints or
    # tool I/O, and combine it with the raw LaTeX content.
    last_user = ""
    for role, content in reversed(messages):
        if role == "user":
            last_user = content
            break

    text_parts: list[str] = []
    if last_user:
        text_parts.append(last_user.lower())
    if latex:
        text_parts.append(latex.lower())
    text = "\n".join(text_parts).strip()

    # Keywords that usually indicate a problem / exercise / proof request.
    # We err slightly on the side of classifying as "solve" so that typical
    # exercise statements like "设 ... 则 X 不完备" are treated as problems
    # rather than pure concept Q&A.
    solve_markers = [
        "证明",
        "试证",
        "试证明",
        "求",
        "计算",
        "求证",
        "解答",
        "题目",
        "例题",
        "例：",
        "exercise",
        "problem",
        "show that",
        "prove that",
        "find",
        "不完备",
        "完备",
        "banach",
        "cauchy",
        "柯西",
    ]

    if any(marker in text for marker in solve_markers):
        return "solve"
    return "qa"


app = FastAPI(title="泛函分析问答与解题小助手 API")


@app.post("/api/functional-analysis/chat", response_model=ChatResponse)
async def functional_analysis_chat(req: ChatRequest) -> ChatResponse:
    """Main chat endpoint for the frontend.

    The frontend sends a simplified chat history and optional LaTeX input.
    We convert this into the message format expected by the LangGraph agent
    and return the agent's full message history along with the final content
    as a convenience.
    """

    try:
        model_name = _resolve_model_name(req.model)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # Convert frontend messages into the (role, content) tuples expected by the
    # LangGraph template.
    lang_messages: list[tuple[str, str]] = [
        (m.role, m.content) for m in req.messages
    ]

    # Hint the inferred task type (Q&A vs solving) to the agent via a short
    # meta-message. This keeps the main prompt in Python while relying on the
    # system prompt for detailed style instructions.
    task_type = _infer_task_type(lang_messages, req.latex)
    if task_type == "qa":
        hint = (
            "当前任务类型: 概念问答。请简明准确地解释相关定义或定理，并尽量与教材符号"
            "保持一致。"
        )
    else:
        hint = (
            "当前任务类型: 解题/证明。请按照教材式的解题风格给出思路和详细解答，"
            "并在关键步骤处使用 [[KEY_STEP ...]] 标记。"
        )
    lang_messages.insert(0, ("user", hint))

    # Only after we have inferred the task type do we append the LaTeX input
    # as an extra user message for the model, so that intent routing is based
    # on the original question text plus the raw LaTeX string.
    if req.latex:
        lang_messages.append(("user", f"LaTeX input:\n{req.latex}"))

    ctx = Context(model=model_name)

    try:
        result = await graph.ainvoke({"messages": lang_messages}, context=ctx)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"模型服务调用失败或连接异常: {type(exc).__name__}: {exc}",
        ) from exc

    # The LangGraph template returns a dict with "messages" holding a list of
    # LangChain message objects. We expose only the final assistant message to
    # the frontend, together with the original user messages, so that internal
    # hints and tool JSON are not shown to the user.
    final_msg = result["messages"][-1]
    final_content = str(final_msg.content)

    frontend_messages: list[FrontendMessage] = [*req.messages]
    frontend_messages.append(
        FrontendMessage(role="assistant", content=final_content)
    )

    return ChatResponse(messages=frontend_messages, raw_content=final_content)


@app.post("/api/functional-analysis/solve-image", response_model=ChatResponse)
async def functional_analysis_solve_image(
    file: UploadFile = File(...),
    model: Literal["deepseek-v3.2", "gpt-5"] = Form("deepseek-v3.2"),
) -> ChatResponse:
    """Placeholder endpoint for image-based problem solving.

    For now we do not run a true vision model. Instead we acknowledge the
    upload and ask the user (via the agent) to provide a textual or LaTeX
    transcription. This keeps the API shape stable so the frontend can
    integrate today, while leaving a clear extension point for future work.
    """

    # Read the file to ensure the upload worked, but we deliberately do not
    # store or process it further here.
    _ = await file.read()

    try:
        model_name = _resolve_model_name(model)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    prompt = (
        "用户上传了一张包含泛函分析题目的图片。由于当前服务尚未集成图像识别，"
        "请先友好地说明这一点，并引导用户用文字或 LaTeX 形式给出题目，再继续解题。"
    )

    ctx = Context(model=model_name)
    result = await graph.ainvoke({"messages": [("user", prompt)]}, context=ctx)

    final_msg = result["messages"][-1]
    final_content = str(final_msg.content)

    frontend_messages: list[FrontendMessage] = []
    for msg in result["messages"]:
        role = getattr(msg, "type", "assistant")
        content = str(getattr(msg, "content", ""))
        if role not in ("user", "assistant"):
            role = "assistant"
        frontend_messages.append(FrontendMessage(role=role, content=content))

    return ChatResponse(messages=frontend_messages, raw_content=final_content)


# Optional convenience entrypoint for local development:
# uv run uvicorn functional_analysis_agent.api:app --reload

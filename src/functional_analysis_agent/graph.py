"""LangGraph ReAct agent for functional analysis Q&A and problem solving."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime

from functional_analysis_agent.context import Context
from functional_analysis_agent.state import InputState, State
from functional_analysis_agent.tools import TOOLS
from functional_analysis_agent.utils import load_chat_model


async def call_model(state: State, runtime: Runtime[Context]) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering the functional analysis agent.

    This prepares the prompt, initializes the model (with tools), and returns
    the model's response.
    """

    model = load_chat_model(runtime.context.model).bind_tools(TOOLS)

    system_message = runtime.context.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": system_message},
                *state.messages,
            ]
        ),
    )

    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content=(
                        "Sorry, I could not construct a satisfactory solution "
                        "within the allowed number of reasoning steps. "
                        "You may try simplifying the question or asking about "
                        "a smaller sub-problem."
                    ),
                )
            ]
        }

    return {"messages": [response]}


builder = StateGraph(State, input_schema=InputState, context_schema=Context)

builder.add_node(call_model)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge("__start__", "call_model")


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output."""

    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, got {type(last_message).__name__}"
        )

    if not last_message.tool_calls:
        return "__end__"

    return "tools"


builder.add_conditional_edges("call_model", route_model_output)

builder.add_edge("tools", "call_model")

graph = builder.compile(name="Functional Analysis ReAct Agent")

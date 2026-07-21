from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState

from app.agent.search_node import search_node
from app.agent.generate_answer_node import generate_answer_node
from app.agent.reasoning_node import reasoning_node
from app.agent.retrieve_knowledge_node import retrieve_knowledge_node
from app.agent.store_knowledge_node import store_knowledge_node
from app.agent.summarization_node import summarization_node

builder = StateGraph(AgentState)

# NODES
builder.add_node("generate_answer", generate_answer_node)
builder.add_node("reasoning",reasoning_node)
builder.add_node("retrieve_knowledge",retrieve_knowledge_node)
builder.add_node("search", search_node)
builder.add_node("store_knowledge", store_knowledge_node)
builder.add_node("summarization", summarization_node)

def route_after_reasoning(state: AgentState):

    if state.should_search:
        return "search"

    return "generate_answer"

builder.add_edge(START, "retrieve_knowledge")

builder.add_edge(
    "retrieve_knowledge",
    "reasoning",
)

builder.add_edge(
    "summarization",
    "store_knowledge",
)

builder.add_edge(
    "store_knowledge",
    "generate_answer",
)

builder.add_edge(
    "generate_answer",
    END,
)

builder.add_conditional_edges(
    "reasoning",
    route_after_reasoning,
    {
        "search": "search",
        "generate_answer": "generate_answer",
    },
)

builder.add_edge("search","summarization")






graph = builder.compile()



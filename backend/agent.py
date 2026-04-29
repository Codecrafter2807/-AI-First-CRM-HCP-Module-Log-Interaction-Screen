import os
import json
from typing import TypedDict, Annotated, Sequence, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from tools import TOOLS

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Initialize the Groq model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY", "mock_key_if_none_provided"), 
    temperature=0,
    max_retries=0
)

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(TOOLS)

def agent_node(state: AgentState):
    """
    Invokes the LLM to process messages and decide if a tool should be called.
    """
    messages = state["messages"]
    
    # System prompt to guide the agent
    sys_prompt = """You are an AI-first CRM assistant.
Your task is to orchestrate specific CRM tools based on the conversation.
1. 'extract_entities' and 'summarize_notes' are INFORMATIVE tools. Call ONLY those tools when requested.
2. ONLY call 'log_interaction' if the user provides a report of a NEW meeting or additional details to save.
3. NAME CONSISTENCY: Always prioritize the specific HCP name mentioned in the conversation history (e.g., 'Dr. Smith'). If no name is mentioned in the current prompt but you are continuing a conversation about a specific person, use that person's name.
4. DO NOT invent or hallucinate names (like 'Dr. Sarah Jenkins') if they are not in the chat history. If the name is unknown, leave it as null.
5. Provide a brief confirmation and STOP.
"""
    
    # We prepend the system prompt
    response = llm_with_tools.invoke([("system", sys_prompt)] + list(messages))
    return {"messages": [response]}

def tool_node(state: AgentState):
    """
    Executes the tool calls made by the LLM.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_responses = []
    
    # Check if the LLM decided to call any tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Find the actual tool function
            tool_fn = next((t for t in TOOLS if t.name == tool_name), None)
            
            if tool_fn:
                # Execute the tool
                try:
                    result = tool_fn.invoke(tool_args)
                except Exception as e:
                    result = json.dumps({"error": str(e)})
                    
                tool_responses.append(
                    ToolMessage(
                        content=str(result),
                        name=tool_name,
                        tool_call_id=tool_call["id"]
                    )
                )
    
    return {"messages": tool_responses}

def should_continue(state: AgentState):
    """
    Determines whether to execute tools or end the conversation loop.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM makes a tool call, we must execute it
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we end the loop and return the response to the user
    return END

# Define the LangGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent") # After tool execution, go back to agent

# Compile the graph
app = workflow.compile()

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
import operator
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()


model=ChatGroq(
    model="llama-3.3-70b-versatile"
)


class message_state(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_llm(state:message_state):
    message=state['messages']
    response=model.invoke(message)
    return {"messages":[response]}

check_point=MemorySaver()
graph=StateGraph(message_state)
graph.add_node("chat_llm",chat_llm)
graph.add_edge(START,"chat_llm")
graph.add_edge("chat_llm",END)

workflow=graph.compile(checkpointer=check_point)

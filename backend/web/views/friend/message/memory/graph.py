# 长期记忆的计算流程图
import os
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph


class MemoryGraph:
    @staticmethod
    def create_app():
        # 连接大模型
        llm = ChatOpenAI(
            model='deepseek-v3.2',
            api_key=os.getenv('API_KEY'),
            base_url=os.getenv('API_BASE'),
        )

        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        # 定义agent节点
        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}
        # 定义状态图
        graph = StateGraph(AgentState)
        # 添加模型调用节点
        graph.add_node('agent', model_call)

        # 添加2条边
        graph.add_edge(START, 'agent')
        graph.add_edge('agent', END)

        return graph.compile()

import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.autoagentsai.graph import FlowGraph, START
from src.autoagentsai.types import QuestionInputState, ForEachState, ConfirmReplyState


def main():
    """循环执行工作流 - 简洁的纯State API"""
    
    # 创建工作流图
    graph = FlowGraph(
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )

    # 设置起始节点 - 直接传State
    graph.add_node(
        id=START,
        state=QuestionInputState()
    )

    # 循环节点 - 直接传State
    graph.add_node(
        id="forEach1",
        state=ForEachState()
    )

    # 确认回复节点 - 直接传State
    graph.add_node(
        id="confirmreply1",
        state=ConfirmReplyState(
            stream=True,
            text="1"
        )
    )

    # 连接节点
    graph.add_edge(START, "forEach1", "userChatInput", "items")
    graph.add_edge(START, "forEach1", "finish", "switchAny")
    graph.add_edge("forEach1", "confirmreply1", "loopStart", "switchAny")
    graph.add_edge("confirmreply1", "forEach1", "finish", "loopEnd")

    # 编译工作流
    graph.compile(
        name="循环执行",
        intro="这是一个专业的循环执行系统",
        category="循环执行",
        prologue="你好！我是你的循环执行系统。"
    )


if __name__ == "__main__":
    main()
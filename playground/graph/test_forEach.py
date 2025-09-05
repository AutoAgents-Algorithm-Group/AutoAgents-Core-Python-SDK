import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.autoagentsai.graph import FlowGraph


def main():
    # 定义工作流对象
    graph = FlowGraph(
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )
    # 添加节点
    # 设置开始节点
    graph.set_start_node(
        position={"x": 0, "y": 300},
    )

    
    uid = uuid.uuid4().hex
    graph.add_node(
        node_id="forEach1",
        module_type="forEach",
        position={"x": 500, "y": 300},
        inputs={
            "index": f"{uid}.index",
            "item": f"{uid}.item",
            "length": f"{uid}.length",
        }
    )

    graph.add_node(
        node_id="confirmreply1",
        module_type="confirmreply",
        position={"x": 1000, "y": 300},
        inputs={
            "stream": True,
            "text": "1"
        }
    )

    graph.add_edge(graph.START, "forEach1", "userChatInput", "items")
    graph.add_edge(graph.START, "forEach1", "finish", "switchAny")
    graph.add_edge("forEach1", "confirmreply1", "loopStart", "switchAny")
    graph.add_edge("confirmreply1", "forEach1", "finish", "loopEnd")


    # print(graph.to_json())

    # 编译
    graph.compile(
        name="循环",
        intro="这是一个专业的代循环执行系统",
        category="循环执行",
        prologue="你好！我是你的循环执行系统。"
    )


if __name__ == "__main__":
    main()

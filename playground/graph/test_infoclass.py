import os
import sys
import uuid

from openpyxl.styles.builtins import output

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.autoagentsai.graph import FlowGraph


def main():
    graph = FlowGraph(
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    graph.add_node(
        node_id="simpleInputId",
        module_type="questionInput",
        position={"x": 0, "y": 300},
        inputs={
            "inputText": True,
            "uploadFile": True,
            "uploadPicture": False,
            "fileContrast": False,
            "initialInput": True
        },
    )
    label1 = str(uuid.uuid1())
    label2 = str(uuid.uuid1())

    graph.add_node(
        node_id="infoclass1",
        module_type="infoClass",
        position={"x": 500, "y": 300},
        inputs={
            "model": "oneapi-deepseek:deepseek-chat",
            "quotePrompt": """
               请扮演文本分类器，根据信息输入和聊天上下文，判断输入信息属于哪种分类，以JSON格式输出分类信息。
            """,
            "labels": {
                label1: "买菜",
                label2: "买肉"
            }
        },
        outputs={
            label1:[
              {
                "targetHandle": "switch",
                "target": "confirmreply1"
              }
            ],
            label2:[
              {
                "targetHandle": "switch",
                "target": "confirmreply2"
              }
            ]

        }
    )
    graph.add_node(
        node_id="confirmreply1",
        module_type="confirmreply",
        position={"x": 1000, "y": 300},
        inputs={
            "text": r"买菜",
            "stream": True
        }
    )
    graph.add_node(
        node_id="confirmreply2",
        module_type="confirmreply",
        position={"x": 1000, "y": 900},
        inputs={
            "text": r"买肉",
            "stream": True
        }
    )
    graph.add_edge("simpleInputId", "infoclass1", "finish", "switchAny")
    graph.add_edge("simpleInputId","infoclass1","userChatInput","text")
    graph.add_edge("infoclass1","confirmreply1",label1,"switchAny")
    graph.add_edge("infoclass1","confirmreply2",label2,"switchAny")


    # print(graph.to_json())

    # 编译,导入配置，点击确定
    graph.compile(
        name="信息分类",
        intro="这是一个专业的信息分类系统",
        category="文档处理",
        prologue="你好！我是你的文档助手。",
        shareAble=True,
        allowVoiceInput=False,
        autoSendVoice=False
    )


if __name__ == "__main__":
    main()

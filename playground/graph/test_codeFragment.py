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
    input_labels = [
        {
            str(uuid.uuid1()): {
                "label": "input啊",
                "valueType": "string"
            }
        }

    ]
    output_labels=[
        {
            str('output_key'): {
                "label": "output啊",
                "valueType": "string"
            }
        }
    ]
    input_label_keys = [list(input_label.keys())[0] for input_label in input_labels]
    output_labels_keys = [list(output_label.keys())[0] for output_label in output_labels]
    graph.add_node(
        node_id="codeFragment1",
        module_type="codeFragment",
        position={"x": 500, "y": 300},
        inputs={
            "model": "doubao-deepseek-v3",
            "_language_": "python",
            "_code_": "def userFunction(params):\n    result = {}\n    result['output_key'] = \"代码块处理了用户输入\"\n    result['input'] = params['" +
                      input_label_keys[0] + "']\n    return result",
            "input_labels": input_labels,
            "output_labels": output_labels
        }
    )

    graph.add_node(
        node_id="confirmreply1",
        module_type="confirmreply",
        position={"x": 1000, "y": 300},
        inputs={
            "stream": True
        }
    )

    graph.add_edge(graph.START, "codeFragment1", "finish", "switchAny")
    graph.add_edge(graph.START, "codeFragment1", "userChatInput", input_label_keys[0])
    graph.add_edge("codeFragment1", "confirmreply1", output_labels_keys[0], "text")

    # print(graph.to_json())

    # 编译
    graph.compile(
        name="代码块",
        intro="这是一个专业的代码块执行系统",
        category="代码块执行",
        prologue="你好！我是你的代码块执行系统。"
    )


if __name__ == "__main__":
    main()

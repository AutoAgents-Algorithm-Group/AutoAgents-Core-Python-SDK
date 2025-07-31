import os
import sys

# 将 `src` 目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.autoagentsai.graph.FlowGraph import FlowGraph
from src.autoagentsai.types import CreateAppParams


def main():
    graph = FlowGraph()

    # 添加节点
    graph.add_node(
        node_id="question1",
        module_type="questionInput",
        position={"x": 0, "y": 100},
        inputs=[
            {"key": "inputText", "value": True},
            {"key": "uploadFile", "value": True},
            {"key": "uploadPicture", "value": False},
            {"key": "fileContrast", "value": False},
            {"key": "initialInput", "value": True}
        ]
    )

    graph.add_node(
        node_id="pdf2md1",
        module_type="pdf2md",
        position={"x": 300, "y": 100},
        inputs=[
            {"key": "pdf2mdType", "value": "deep_pdf2md"}
        ]
    )
    memory_variable_inputs = []
    input_1 = {
        "key": "test1",
        "label": "test1",
        "value_type": "String"
    }
    input_2 = {
        "key": "test2",
        "label": "test2",
        "value_type": "Boolean"
    }

    memory_variable_inputs.append(input_1)
    memory_variable_inputs.append(input_2)

    graph.add_node(
        node_id="addMemoryVariable1",
        module_type="addMemoryVariable",
        position={"x": 1500, "y": 300},
        inputs=memory_variable_inputs
    )
    graph.add_node(
        node_id="memory1",
        module_type="addMemoryVariable",
        position={"x": 600, "y": 100},
        inputs=[
            {"key": "parsedText", "type": "agentMemoryVar", "value": ""}
        ]
    )

    graph.add_node(
        node_id="ai1",
        module_type="aiChat",
        position={"x": 900, "y": 100},
        inputs=[
            {"key": "model", "value": "glm-4-airx"},
            {"key": "quotePrompt",
             "value": "你是一个专业文档助手，请根据以下文档内容回答问题：\n【文档内容】\n\n\n【用户问题】\n"},
            {"key": "temperature", "value": 0.2},
            {"key": "historyText", "value": 0}
        ]
    )

    graph.add_node(
        node_id="reply1",
        module_type="confirmreply",
        position={"x": 1200, "y": 100},
        inputs=[
            {"key": "stream", "value": True}
        ]
    )

    # 添加连接边
    graph.add_edge("question1", "pdf2md1", "finish", "switchAny")
    graph.add_edge("question1", "ai1", "userChatInput", "text")
    graph.add_edge("pdf2md1", "memory1", "pdf2mdResult", "parsedText")
    graph.add_edge("pdf2md1", "ai1", "finish", "switchAny")
    graph.add_edge("ai1", "reply1", "answerText", "text")
    graph.add_edge("ai1", "reply1", "finish", "switchAny")

    print(graph.to_json())

    graph.compile(CreateAppParams())

if __name__ == "__main__":
    main()
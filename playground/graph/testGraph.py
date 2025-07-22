import os
import sys

# 将 `src` 目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.autoagentsai.graph.FlowGraph import FlowGraph
from src.autoagentsai.types import CreateAppParams


def main():
    graph = FlowGraph()

    graph.add_node(
        node_id="question1",
        module_type="questionInput",
        position={"x": 0, "y": 100},
        inputs=[
            {"key": "inputText", "value": True},
            {"key": "uploadFile", "value": True},
            {"key": "uploadPicture", "value": False},
            {"key": "fileUpload", "value": False},
            {"key": "fileContrast", "value": False}
        ]
    )

    graph.add_node(
        node_id="pdf2md1",
        module_type="pdf2md",
        position={"x": 300, "y": 100},
        inputs=[{"key": "pdf2mdType", "value": "deep_pdf2md"}]
    )

    graph.add_node(
        node_id="ai1",
        module_type="aiChat",
        position={"x": 600, "y": 100},
        inputs=[
            {"key": "model", "value": "glm-4-airx"},
            {"key": "quotePrompt", "value": "你是一个专业文档助手，请严格根据以下文档内容回答问题：\n{{text}}"},
            {"key": "temperature", "value": 0},
            {"key": "historyText", "value": 0}
        ]
    )

    graph.add_node(
        node_id="memory1",
        module_type="addMemoryVariable",
        position={"x": 900, "y": 100},
        inputs=[{"key": "feedback", "value": "{{answerText}}"}]
    )

    graph.add_node(
        node_id="confirm1",
        module_type="confirmreply",
        position={"x": 1200, "y": 100},
        inputs=[{"key": "text", "value": "{{question}}"}]
    )

    graph.add_edge("question1", "pdf2md1", "files", "files")
    graph.add_edge("question1", "pdf2md1", "finish", "switchAny")
    graph.add_edge("pdf2md1", "ai1", "pdf2mdResult", "text")
    graph.add_edge("pdf2md1", "ai1", "finish", "switchAny")
    graph.add_edge("ai1", "memory1", "answerText", "feedback")
    graph.add_edge("ai1", "confirm1", "finish", "switchAny")

    print(graph.to_json())

    graph.compile(CreateAppParams())

if __name__ == "__main__":
    main()
import os
import sys
import json

# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.autoagentsai.graph.FlowGraph import FlowGraph
from src.autoagentsai.types import CreateAppParams


def main():
    graph = FlowGraph()

    # 添加一个带有多个记忆变量的 addMemoryVariable 节点
    graph.add_node(
        node_id="memory1",
        module_type="addMemoryVariable",
        position={"x": 900, "y": 100},
        inputs=[
            {
                "key": "feedback",
                "valueType": "string",
            },
            {
                "key": "question",
                "valueType": "string",
            },
            {
                "key": "timestamp",
                "valueType": "string",
            }
        ]
    )

    # 输出节点的JSON表示，检查inputs是否正确
    node_json = json.dumps(graph.nodes[0].to_dict(), indent=2, ensure_ascii=False)
    print("节点JSON:")
    print(node_json)

    # 检查inputs是否包含所有三个变量
    inputs = graph.nodes[0].data["inputs"]
    print(f"\n输入变量数量: {len(inputs)}")
    
    # 打印每个输入变量的信息
    for i, input_var in enumerate(inputs):
        print(f"\n变量 {i+1}:")
        print(f"  键名: {input_var.get('key')}")
        print(f"  标签: {input_var.get('label')}")
        print(f"  值: {input_var.get('value')}")
        print(f"  类型: {input_var.get('type')}")


if __name__ == "__main__":
    main()
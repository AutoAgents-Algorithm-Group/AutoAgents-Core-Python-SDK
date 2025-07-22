import uuid
import json
from copy import deepcopy

import requests
from ..api.ChatApi import get_jwt_token_api
from .template_registry import NODE_TEMPLATES
from ..types import CreateAppParams


class FlowNode:
    def __init__(self, node_id, module_type, position, inputs=None, outputs=None):
        self.id = node_id
        self.type = "custom"
        self.initialized = False
        self.position = position
        self.data = {
            "inputs": inputs or [],
            "outputs": outputs or [],
            "disabled": False,
            "moduleType": module_type,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "initialized": self.initialized,
            "position": self.position,
            "data": self.data
        }

class FlowEdge:
    def __init__(self, source, target, source_handle="", target_handle=""):
        self.id = str(uuid.uuid4())
        self.type = "custom"
        self.source = source
        self.target = target
        self.sourceHandle = source_handle
        self.targetHandle = target_handle
        self.data = {}
        self.label = ""
        self.animated = False
        self.sourceX = 0
        self.sourceY = 0
        self.targetX = 0
        self.targetY = 0

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "target": self.target,
            "sourceHandle": self.sourceHandle,
            "targetHandle": self.targetHandle,
            "data": self.data,
            "label": self.label,
            "animated": self.animated,
            "sourceX": self.sourceX,
            "sourceY": self.sourceY,
            "targetX": self.targetX,
            "targetY": self.targetY
        }

class FlowGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.viewport = {"x": 0, "y": 0, "zoom": 1.0}

    def add_node(self, node_id, module_type, position, inputs=None, outputs=None):
        tpl = deepcopy(NODE_TEMPLATES.get(module_type))
        final_inputs = self.merge_template_io(tpl.get("inputs", []), inputs)
        final_outputs = self.merge_template_io(tpl.get("outputs", []), outputs)
        node = FlowNode(
            node_id=node_id,
            module_type=module_type,
            position=position,
            inputs=final_inputs,
            outputs=final_outputs
        )
        node.data["name"]=tpl.get("name")
        node.data["intro"] = tpl.get("intro")
        if tpl.get("category") is not None:
            node.data["category"] = tpl["category"]
        self.nodes.append(node)

    def add_edge(self, source, target, source_handle="", target_handle=""):
        edge = FlowEdge(source, target, source_handle, target_handle)
        self.edges.append(edge)

    def to_json(self):
        return json.dumps({
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "viewport": self.viewport
        }, indent=2, ensure_ascii=False)

    def set_viewport(self, x, y, zoom):
        self.viewport = {"x": x, "y": y, "zoom": zoom}

    def merge_template_io(self,template_io, custom_io):
        # 参数说明：
        # template_io：模板中inputs或outputs列表，每个元素是一个字段的字典，字段完整
        # custom_io：用户传入的inputs或outputs列表，通常是部分字段，可能只有部分key覆盖

        if not custom_io:
            # 如果用户没有传自定义字段，直接返回模板的完整字段（深拷贝避免修改原数据）
            return deepcopy(template_io)

        merged = []
        # 遍历模板里的所有字段
        for t_item in template_io:
            # 在用户自定义列表中找有没有和当前模板字段 key 一样的字段
            c_item = next((c for c in custom_io if c.get("key") == t_item.get("key")), None)

            if c_item:
                # 找到了用户自定义字段
                merged_item = deepcopy(t_item)  # 先复制模板字段（保证完整结构）
                merged_item.update(c_item)  # 用用户的字段内容覆盖模板字段（例如value、description等被覆盖）
                merged.append(merged_item)
            else:
                # 用户没定义，直接用模板字段完整拷贝
                merged.append(deepcopy(t_item))

        return merged

    def post_with_jwt(self, data: CreateAppParams, base_url: str = "https://uat.agentspro.cn") -> requests.Response:
        # 获取 JWT Token，假设get_jwt_token_api需要这两个参数
        jwt_token = get_jwt_token_api("135c9b6f7660456ba14a2818a311a80e", "i34ia5UpBnjuW42huwr97xTiFlIyeXc7")

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        url=f"{base_url}/api/agent/create"
        data.appModel=self.to_json()
        if not data.name:
            data.name = "test"
        response = requests.post(url, json=data.model_dump(), headers=headers)
        # 判断请求结果
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("code") == 1:
                # 成功，返回接口响应内容（包含知识库ID等信息）
                print("创建成功")
                return response_data
            else:
                raise Exception(f"创建智能体失败: {response_data.get('msg', 'Unknown error')}")
        else:
            raise Exception(f"创建智能体失败: {response.status_code} - {response.text}")

    def compile(self):
        self.post_with_jwt(data=CreateAppParams())


if __name__ == "__main__":

    import requests
    import json
    import textwrap

    # 你的完整代码字符串，多行用三引号写，保持格式
    code_str = textwrap.dedent("""
    from src.autoagentsai.graph import FlowGraph
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
            {"key": "fileContrast", "value": False}
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

    graph.add_node(
        node_id="knowledgesSearch1",
        module_type="knowledgesSearch",
        position={"x": 600, "y": 100},
        inputs=[
            {"key": "datasets", "value": ["智能体知识库"]},
            {"key": "similarity", "value": 0.65},
            {"key": "topK", "value": 5}
        ]
    )

    graph.add_node(
        node_id="aiChat1",
        module_type="aiChat",
        position={"x": 900, "y": 100},
        inputs=[
            {"key": "model", "value": "glm-4-airx"},
            {"key": "quotePrompt", "value": "你是一个专业文档助手，请根据以下知识库内容回答问题：\\n{{knSearch}}"},
            {"key": "temperature", "value": 0.1}
        ]
    )

    graph.add_node(
        node_id="confirmreply1",
        module_type="confirmreply",
        position={"x": 1200, "y": 100},
        inputs=[
            {"key": "text", "value": "当前文档未包含相关答案，请尝试重新提问或上传更详细的资料"}
        ]
    )

    # 添加连接边
    graph.add_edge(
        source="question1",
        target="pdf2md1",
        source_handle="files",
        target_handle="files"
    )

    graph.add_edge(
        source="question1",
        target="pdf2md1",
        source_handle="finish",
        target_handle="switchAny"
    )

    graph.add_edge(
        source="pdf2md1",
        target="knowledgesSearch1",
        source_handle="pdf2mdResult",
        target_handle="text"
    )

    graph.add_edge(
        source="pdf2md1",
        target="knowledgesSearch1",
        source_handle="finish",
        target_handle="switchAny"
    )

    graph.add_edge(
        source="knowledgesSearch1",
        target="aiChat1",
        source_handle="quoteQA",
        target_handle="knSearch"
    )

    graph.add_edge(
        source="knowledgesSearch1",
        target="aiChat1",
        source_handle="unEmpty",
        target_handle="switchAny"
    )

    graph.add_edge(
        source="knowledgesSearch1",
        target="confirmreply1",
        source_handle="isEmpty",
        target_handle="switchAny"
    )

    graph.add_edge(
        source="aiChat1",
        target="confirmreply1",
        source_handle="answerText",
        target_handle="text"
    )

    graph.add_edge(
        source="aiChat1",
        target="confirmreply1",
        source_handle="finish",
        target_handle="switchAny"
    )

    print(graph.to_json())

    graph.compile()
    """)

    # 构造请求体，requests 会帮你自动转义成正确 JSON 格式
    payload = {"code": code_str}

    # 接口地址
    url = "http://127.0.0.1:8000/run"

    # 发送 POST 请求
    response = requests.post(url, json=payload)

    # 输出响应
    print("状态码:", response.status_code)
    try:
        print("响应内容:", response.json())
    except Exception:
        print("响应文本:", response.text)
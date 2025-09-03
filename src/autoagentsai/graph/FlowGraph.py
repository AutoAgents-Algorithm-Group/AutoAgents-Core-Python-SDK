import json
import uuid
from copy import deepcopy
from typing import Optional, List, Dict, Tuple

from .NodeRegistry import NODE_TEMPLATES, merge_template_io
from ..api.GraphApi import create_app_api, process_add_memory_variable
from ..types.GraphTypes import CreateAppParams
from ..utils.convertor import convert_json_to_json_list


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
    def __init__(self, personal_auth_key: str, personal_auth_secret: str, base_url: str = "https://uat.agentspro.cn"):
        """
        初始化 FlowGraph

        Args:
            personal_auth_key: 个人认证密钥
            personal_auth_secret: 个人认证密码
            base_url: API 基础URL，默认为 "https://uat.agentspro.cn"
        """
        self.nodes = []
        self.edges = []
        self.viewport = {"x": 0, "y": 0, "zoom": 1.0}

        # 保存认证信息
        self.personal_auth_key = personal_auth_key
        self.personal_auth_secret = personal_auth_secret
        self.base_url = base_url

    def add_node(self, node_id, module_type, position, inputs=None, outputs=None):
        tpl = deepcopy(NODE_TEMPLATES.get(module_type))

        if module_type == "addMemoryVariable":
            final_inputs = process_add_memory_variable(tpl.get("inputs", [])[0], inputs)
            final_outputs = []
        else:
            # 转换简洁格式为展开格式
            converted_inputs = convert_json_to_json_list(inputs)
            converted_outputs = convert_json_to_json_list(outputs)
            final_inputs = merge_template_io(tpl.get("inputs", []), converted_inputs)
            final_outputs = merge_template_io(tpl.get("outputs", []), converted_outputs)

            if module_type == "infoClass":
                if outputs is not None:
                    for key, value in outputs.items():
                        # outputs里元素如果是labels相关的才会添加
                        if 'target' in list(value[0].keys()) and 'targetHandle' in list(value[0].keys()):
                            final_outputs.append({
                                "valueType": "boolean",
                                "type": "source",
                                "key": key,
                                "targets": value
                            })

        node = FlowNode(
            node_id=node_id,
            module_type=module_type,
            position=position,
            inputs=final_inputs,
            outputs=final_outputs
        )
        node.data["name"] = tpl.get("name")
        node.data["intro"] = tpl.get("intro")
        if tpl.get("category") is not None:
            node.data["category"] = tpl["category"]
        self.nodes.append(node)

    def add_edge(self, source, target, source_handle="", target_handle=""):
        source_handle, target_handle = self._check_and_fix_handle_type(source, target, source_handle, target_handle)
        edge = FlowEdge(source, target, source_handle, target_handle)
        self.edges.append(edge)

    def to_json(self):
        return json.dumps({
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "viewport": self.viewport
        }, indent=2, ensure_ascii=False)

    def update_node(self):
        update = []
        for edge in self.edges:
            # print(edge)
            for i in range(len(self.nodes)):
                node = self.nodes[i]
                # print(node.data['outputs'])
                if node.id == edge.source:
                    # print(node.i)
                    for dot in node.data['outputs']:
                        for k, v in dot.items():
                            if v == edge.sourceHandle:
                                # print(edge.sourceHandle)
                                flag = {
                                    "node_id": node.id,
                                    "key": dot['key'],
                                    "targets": [
                                        {
                                            "targetHandle": edge.targetHandle,
                                            "target": edge.target
                                        }
                                    ]
                                }
                                update.append(flag)
        # 聚合并应用到 nodes 的 outputs.targets
        # 1) 聚合：按 node_id 与 key 合并多个 targets
        aggregated: Dict[str, Dict[str, List[Dict]]] = {}
        for item in update:
            node_id = item.get("node_id")
            key = item.get("key")
            targets = item.get("targets", [])
            if not node_id or not key:
                continue
            if node_id not in aggregated:
                aggregated[node_id] = {}
            if key not in aggregated[node_id]:
                aggregated[node_id][key] = []
            aggregated[node_id][key].extend(targets)
        # print(aggregated)
        """
        {'simpleInputId': {'finish': [{'targetHandle': 'switchAny', 'target': 'infoclass1'}], 'userChatInput': [{'targetHandle': 'text', 'target': 'infoclass1'}]}, 'infoclass1': {'e6d6e7f2-88b0-11f0-820f-8a9feca29835': [{'targetHandle': 'switchAny', 'target': 'confirmreply1'}], 'e6d6e8ba-88b0-11f0-820f-8a9feca29835': [{'targetHandle': 'switchAny', 'target': 'confirmreply2'}]}}
        """
        # 2) 应用：遍历 nodes，定位对应 output.key，替换/设置其 targets
        for node in self.nodes:
            node_updates = aggregated.get(node.id)
            if not node_updates:
                continue
            # print(node_updates)
            outputs = node.data.get("outputs", [])
            for output in outputs:
                output_key = output.get("key")
                if output_key in node_updates:
                    # 去重：同一目标去重（按 target 与 targetHandle）
                    combined = node_updates[output_key]
                    unique = []
                    seen = set()
                    for t in combined:
                        tup = (t.get("target"), t.get("targetHandle"))
                        if tup not in seen:
                            seen.add(tup)
                            unique.append({"target": t.get("target"), "targetHandle": t.get("targetHandle")})
                    output["targets"] = unique

    def compile(self,
                name: str = "未命名智能体",  # 智能体名称
                avatar: str = "https://uat.agentspro.cn/assets/agent/avatar.png",  # 头像URL
                intro: Optional[str] = None,  # 智能体介绍
                chatAvatar: Optional[str] = None,  # 对话头像URL
                shareAble: Optional[bool] = None,  # 是否可分享
                guides: Optional[List] = None,  # 引导配置
                category: Optional[str] = None,  # 分类
                state: Optional[int] = None,  # 状态
                prologue: Optional[str] = None,  # 开场白
                extJsonObj: Optional[Dict] = None,  # 扩展JSON对象
                allowVoiceInput: Optional[bool] = None,  # 是否允许语音输入
                autoSendVoice: Optional[bool] = None,  # 是否自动发送语音
                **kwargs) -> None:  # 其他参数
        """
        编译并创建智能体应用
        """

        # 更新node里面的targets
        self.update_node()

        data = CreateAppParams(
            name=name,
            avatar=avatar,
            intro=intro,
            chatAvatar=chatAvatar,
            shareAble=shareAble,
            guides=guides,
            appModel=self.to_json(),  # 自动设置工作流JSON
            category=category,
            state=state,
            prologue=prologue,
            extJsonObj=extJsonObj,
            allowVoiceInput=allowVoiceInput,
            autoSendVoice=autoSendVoice,
            **kwargs
        )

        create_app_api(data, self.personal_auth_key, self.personal_auth_secret, self.base_url)

    def _check_and_fix_handle_type(self, source: str, target: str, source_handle: str, target_handle: str) -> Tuple[
        str, str]:
        """
        检查 source_handle 与 target_handle 是否类型一致。
        若不一致，则清空 target_handle。
        """
        source_type = self._get_field_type_from_source(source, source_handle)
        target_type = self._get_field_type_from_target(target, target_handle)

        return (
            source_handle,
            target_handle if source_handle and target_handle and source_type == target_type else ""
        )

    def _get_field_type_from_source(self, node_id: str, field_key: str) -> Optional[str]:
        """
        从节点列表中查找 node_id 对应节点的字段类型（valueType）
        """
        for node in self.nodes:
            if node.id == node_id:
                for field in node.data.get("outputs", []):
                    if field.get("key") == field_key:
                        return field.get("valueType")
                break
        return None

    def _get_field_type_from_target(self, node_id: str, field_key: str) -> Optional[str]:
        """
        从节点列表中查找 node_id 对应节点的字段类型（valueType）
        """
        for node in self.nodes:
            if node.id == node_id:
                for field in node.data.get("inputs", []):
                    if field.get("key") == field_key:
                        return field.get("valueType")
                break
        return None

    @staticmethod
    def from_json_to_code(json_data: dict, auth_key: str = "your_auth_key",
                          auth_secret: str = "your_auth_secret",
                          base_url: str = "https://uat.agentspro.cn"):
        """
        将JSON格式的流程图数据转换为SDK代码

        Args:
            json_data: 包含nodes和edges的JSON数据
            auth_key: 认证密钥
            auth_secret: 认证密码
            base_url: API基础URL

        Returns:
            生成的Python SDK代码字符串
        """

        def extract_custom_inputs(node_data: dict) -> dict:
            """提取用户自定义的inputs，包含所有用户明确指定的参数"""
            module_type = node_data.get("moduleType")
            template = NODE_TEMPLATES.get(module_type, {})
            template_inputs = template.get("inputs", [])
            node_inputs = node_data.get("inputs", [])

            custom_inputs = {}

            if module_type == "addMemoryVariable":
                # 特殊处理addMemoryVariable
                memory_vars = []
                for inp in node_inputs:
                    if inp.get("type") == "agentMemoryVar":
                        memory_vars.append({
                            "key": inp.get("key"),
                            "value_type": inp.get("valueType", "String")
                        })
                return memory_vars

            # 创建模板字段的映射，包含类型信息
            template_fields = {}
            for template_input in template_inputs:
                key = template_input.get("key")
                template_fields[key] = {
                    "default_value": template_input.get("value"),
                    "type": template_input.get("type"),
                    "keyType": template_input.get("keyType")
                }

            # 提取用户明确指定的参数值
            for node_input in node_inputs:
                key = node_input.get("key")
                value = node_input.get("value")

                # 跳过trigger相关的系统字段
                if key in template_fields:
                    field_info = template_fields[key]
                    key_type = field_info.get("keyType")
                    field_type = field_info.get("type")

                    # 跳过trigger类型的字段（这些是系统字段）
                    if key_type in ["trigger", "triggerAny"]:
                        continue

                    # 跳过target类型但不是用户输入的字段
                    if field_type == "target" and key not in ["text", "images", "files", "knSearch"]:
                        continue

                # 包含用户明确指定的所有参数值
                if "value" in node_input:
                    custom_inputs[key] = value

            return custom_inputs

        def format_value(value) -> str:
            """格式化Python值"""
            if isinstance(value, str):
                # 处理多行字符串
                if '\n' in value:
                    # 使用三重引号处理多行字符串
                    escaped_value = value.replace('\\', '\\\\').replace('"""', '\\"""')
                    return f'"""{escaped_value}"""'
                else:
                    # 处理单行字符串，转义引号
                    escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                    return f'"{escaped_value}"'
            elif isinstance(value, bool):
                return str(value)
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, list):
                return str(value)
            elif isinstance(value, dict):
                return str(value)
            else:
                return f'"{str(value)}"'

        def generate_node_code(node: dict) -> str:
            """生成单个节点的代码"""
            node_id = node.get("id")
            module_type = node["data"].get("moduleType")
            position = node.get("position", {"x": 0, "y": 0})

            custom_inputs = extract_custom_inputs(node["data"])

            if module_type == "addMemoryVariable":
                # 特殊处理addMemoryVariable
                code_lines = []
                code_lines.append(f"    memory_variable_inputs = []")

                for var in custom_inputs:
                    var_name = var["key"]
                    var_type = var["value_type"]
                    code_lines.append(f"    {var_name} = {{")
                    code_lines.append(f'        "key": "{var_name}",')
                    code_lines.append(f'        "value_type": "{var_type}"')
                    code_lines.append(f"    }}")
                    code_lines.append(f"    memory_variable_inputs.append({var_name})")

                code_lines.append("")
                code_lines.append(f"    graph.add_node(")
                code_lines.append(f'        node_id="{node_id}",')
                code_lines.append(f'        module_type="{module_type}",')
                code_lines.append(f"        position={position},")
                code_lines.append(f"        inputs=memory_variable_inputs")
                code_lines.append(f"    )")

                return "\n".join(code_lines)
            else:
                # 普通节点处理
                code_lines = []
                code_lines.append(f"    graph.add_node(")
                code_lines.append(f'        node_id="{node_id}",')
                code_lines.append(f'        module_type="{module_type}",')
                code_lines.append(f"        position={position},")

                if custom_inputs:
                    code_lines.append(f"        inputs={{")
                    for key, value in custom_inputs.items():
                        formatted_value = format_value(value)
                        code_lines.append(f'            "{key}": {formatted_value},')
                    code_lines.append(f"        }}")

                code_lines.append(f"    )")

                return "\n".join(code_lines)

        def generate_edge_code(edge: dict) -> str:
            """生成单个边的代码"""
            source = edge.get("source")
            target = edge.get("target")
            source_handle = edge.get("sourceHandle", "")
            target_handle = edge.get("targetHandle", "")

            return f'    graph.add_edge("{source}", "{target}", "{source_handle}", "{target_handle}")'

        # 生成代码
        code_lines = []

        # 导入和初始化部分
        code_lines.append("from autoagentsai.graph import FlowGraph")
        code_lines.append("")
        code_lines.append("")
        code_lines.append("def main():")
        code_lines.append("    graph = FlowGraph(")
        code_lines.append(f'            personal_auth_key="{auth_key}",')
        code_lines.append(f'            personal_auth_secret="{auth_secret}",')
        code_lines.append(f'            base_url="{base_url}"')
        code_lines.append("        )")
        code_lines.append("")

        # 生成节点代码
        code_lines.append("    # 添加节点")
        nodes = json_data.get("nodes", [])
        for node in nodes:
            code_lines.append(generate_node_code(node))
            code_lines.append("")

        # 生成边代码
        code_lines.append("    # 添加连接边")
        edges = json_data.get("edges", [])
        for edge in edges:
            code_lines.append(generate_edge_code(edge))

        code_lines.append("")
        code_lines.append("    # 编译,导入配置，点击确定")
        code_lines.append("    graph.compile(")
        code_lines.append('            name="从JSON生成的工作流",')
        code_lines.append('            intro="这是从JSON数据反向生成的工作流",')
        code_lines.append('            category="自动生成",')
        code_lines.append('            prologue="你好！这是自动生成的工作流。",')
        code_lines.append('            shareAble=True,')
        code_lines.append('            allowVoiceInput=False,')
        code_lines.append('            autoSendVoice=False')
        code_lines.append("        )")
        code_lines.append("")
        code_lines.append('if __name__ == "__main__":')
        code_lines.append("    main()")

        return "\n".join(code_lines)
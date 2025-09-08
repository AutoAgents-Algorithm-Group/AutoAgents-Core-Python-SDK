import json
import uuid
from copy import deepcopy
from typing import Optional, List, Dict, Tuple

from .NodeRegistry import NODE_TEMPLATES, merge_template_io
from .StateConverter import create_node_from_state, state_to_module_type, state_to_inputs_outputs
from ..api.GraphApi import create_app_api, process_add_memory_variable
from ..types.GraphTypes import CreateAppParams
from ..types.NodeStates import BaseNodeState
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
        # 结构信息
        self.nodes = []
        self.edges = []
        self.viewport = {"x": 0, "y": 0, "zoom": 1.0}

        # 开始与结束节点ID
        self.START = "simpleInputId"
        self.END = None
        
        # 认证信息
        self.personal_auth_key = personal_auth_key
        self.personal_auth_secret = personal_auth_secret
        self.base_url = base_url

    def add_start_node(self, *, position: dict = None, state):
        """
        设置工作流的起始节点（questionInput类型）
        起始节点ID固定为"simpleInputId"
        
        Args:
            position: 节点位置，默认为{"x": 0, "y": 300}
            state: QuestionInputState状态对象
            
        Usage:
            start_state = QuestionInputState(inputText=True, uploadFile=True)
            graph.set_start_node(position={"x": 0, "y": 300}, state=start_state)
            
            # 位置可以省略
            graph.set_start_node(state=start_state)
        """
        if position is None:
            position = {"x": 0, "y": 300}
            
        self.add_node(
            id=self.START,
            position=position,
            state=state
        )


    def add_memory_variables(self, id: str, *, position: dict = None, state):
        """
        添加记忆变量节点的简化方法
        
        Args:
            id: 节点ID
            position: 节点位置，默认为{"x": 0, "y": 1500}
            state: AddMemoryVariableState状态对象
            
        Usage:
            state = AddMemoryVariableState(variables={
                "user_input": "string", 
                "ai_response": "string"
            })
            graph.add_memory_variables("memory1", state=state)
            
            # 位置可以省略，将自动布局
            graph.add_memory_variables("memory1", state=state)
        """
        if position is None:
            position = {"x": 0, "y": 1500}
            
        self.add_node(
            id=id,
            position=position,
            state=state
        )

    def add_node(self, id: str, *, position=None, state):
        """
        添加节点到工作流图中
        
        Args:
            id: 节点ID
            position: 节点位置，格式为 {"x": 100, "y": 200}，默认自动布局
            state: 节点状态对象（LangGraph风格）
            
        Usage:
            state = AiChatState(model="doubao-deepseek-v3", text="hello", temperature=0.7)
            graph.add_node("node1", position={"x": 100, "y": 200}, state=state)
            
            # 位置可以省略，将自动布局
            graph.add_node("node2", state=InfoClassState(labels={"A": "选项A"}))
        """
        
        # 验证state参数
        if not isinstance(state, BaseNodeState):
            raise ValueError("state parameter must be an instance of BaseNodeState")
            
        # 自动布局位置（如果没有提供）
        if position is None:
            # 简单的自动布局：水平排列，每个节点间距300px
            position = {"x": len(self.nodes) * 500, "y": 300}
            
        # 从state中提取所有配置
        extracted_node_id, extracted_module_type, extracted_position, extracted_inputs, extracted_outputs = create_node_from_state(
            state, id, position
        )
        
        # 使用从state提取的配置
        module_type = extracted_module_type
        inputs = extracted_inputs
        outputs = extracted_outputs
        
        # 特殊处理addMemoryVariable的情况
        if module_type == "addMemoryVariable" and isinstance(extracted_inputs, list):
            # 对于addMemoryVariable，extracted_inputs是特殊格式的列表
            return self._add_memory_variable_from_state(id, position, extracted_inputs)
            
        tpl = deepcopy(NODE_TEMPLATES.get(module_type))

        if module_type == "addMemoryVariable":
            final_inputs = process_add_memory_variable(tpl.get("inputs", [])[0],inputs)
            final_outputs = []
        else:
            # 对于infoClass类型，预处理labels字段并自动生成outputs
            infoclass_output_keys = []
            if module_type == "infoClass":
                if inputs and "labels" in inputs:
                    inputs = deepcopy(inputs)  # 避免修改原始输入
                    original_labels = inputs["labels"]
                    inputs["labels"] = self._convert_labels_dict_to_list(original_labels)
                    
                    # 自动从labels提取输出标签
                    if isinstance(original_labels, dict):
                        infoclass_output_keys = list(original_labels.keys())
                    elif isinstance(original_labels, list):
                        # 如果是数组格式 [{"key": key1, "value": "value1"}]
                        infoclass_output_keys = [item.get("key") for item in original_labels if item.get("key")]
                
                # infoClass不需要用户手动指定outputs，自动从labels生成
                outputs = None
            
            # codeFragment：解析 input_labels / output_labels 为参数型 inputs/outputs
            # 通过统一的解析函数转换为JSON模板所需的参数定义结构
            codefragment_param_inputs = []
            codefragment_param_outputs = []
            if module_type == "codeFragment" and inputs and isinstance(inputs, dict):
                inputs = deepcopy(inputs)  # 避免修改原始输入
                parsed_inputs, parsed_outputs = self._parse_codefragment_labels(inputs)
                codefragment_param_inputs.extend(parsed_inputs)
                codefragment_param_outputs.extend(parsed_outputs)
            
            # 转换简洁格式为展开格式
            converted_inputs = convert_json_to_json_list(inputs)
            converted_outputs = convert_json_to_json_list(outputs)
            final_inputs = merge_template_io(tpl.get("inputs", []), converted_inputs)
            final_outputs = merge_template_io(tpl.get("outputs", []), converted_outputs)

            # 追加由 labels 生成的参数输入/输出
            if module_type == "codeFragment" and codefragment_param_inputs:
                final_inputs.extend(codefragment_param_inputs)
            if module_type == "codeFragment" and codefragment_param_outputs:
                final_outputs.extend(codefragment_param_outputs)

            if module_type == "infoClass" and infoclass_output_keys:
                for key in infoclass_output_keys:
                    # 为infoClass的每个标签添加输出字段，targets将通过add_edge自动构建
                    final_outputs.append({
                        "valueType": "boolean",
                        "type": "source",
                        "key": key,
                        "targets": []  # 初始为空，通过update_node从edges自动构建
                    })


        node = FlowNode(
            node_id=id,
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
        
    def _add_memory_variable_from_state(self, id: str, position: Dict[str, float], memory_inputs: List[Dict[str, str]]):
        """
        从state添加记忆变量节点的特殊处理方法
        
        Args:
            node_id: 节点ID
            position: 节点位置
            memory_inputs: 记忆变量输入列表
        """
        tpl = deepcopy(NODE_TEMPLATES.get("addMemoryVariable"))
        final_inputs = process_add_memory_variable(tpl.get("inputs", [])[0], memory_inputs)
        final_outputs = []
        
        node = FlowNode(
            node_id=id,
            module_type="addMemoryVariable",
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
        source_handle, target_handle= self._check_and_fix_handle_type(source, target, source_handle, target_handle)
        edge = FlowEdge(source, target, source_handle, target_handle)
        self.edges.append(edge)

    def to_json(self):
        return json.dumps(
            {
                "nodes": [node.to_dict() for node in self.nodes],
                "edges": [edge.to_dict() for edge in self.edges],
                "viewport": self.viewport
            }, 
            indent=2, 
            ensure_ascii=False
        )

    def _update_node(self):
        """
        高效更新节点的输出连接目标
        时间复杂度: O(edges + nodes + outputs) vs 原来的 O(edges * nodes * outputs)
        """
        # 1. 构建节点索引，避免线性搜索
        node_map = {node.id: node for node in self.nodes}
        
        # 2. 构建输出键到输出对象的映射，便于快速定位
        output_map = {}  # {node_id: {output_key: output_object}}
        for node in self.nodes:
            output_map[node.id] = {}
            for output in node.data.get("outputs", []):
                output_key = output.get("key")
                if output_key:
                    output_map[node.id][output_key] = output
        
        # 3. 构建连接映射：直接从边构建最终的连接关系
        connections = {}  # {node_id: {output_key: [target_info]}}
        
        for edge in self.edges:
            source_node = node_map.get(edge.source)
            if not source_node:
                continue
                
            # 查找匹配的输出键
            source_output_key = self._find_output_key_by_handle(source_node, edge.sourceHandle)
            if not source_output_key:
                continue
                
            # 构建目标信息
            target_info = {
                "target": edge.target,
                "targetHandle": edge.targetHandle
            }
            
            # 添加到连接映射中
            if edge.source not in connections:
                connections[edge.source] = {}
            if source_output_key not in connections[edge.source]:
                connections[edge.source][source_output_key] = []
            connections[edge.source][source_output_key].append(target_info)
        
        # 4. 去重并应用连接关系到节点
        for node_id, node_connections in connections.items():
            for output_key, targets in node_connections.items():
                # 去重：使用set去除重复的连接
                unique_targets = []
                seen = set()
                for target in targets:
                    target_tuple = (target["target"], target["targetHandle"])
                    if target_tuple not in seen:
                        seen.add(target_tuple)
                        unique_targets.append(target)
                
                # 应用到对应的输出对象
                if node_id in output_map and output_key in output_map[node_id]:
                    output_map[node_id][output_key]["targets"] = unique_targets
    
    def _find_output_key_by_handle(self, node, source_handle):
        """
        根据source_handle查找对应的输出键
        
        Args:
            node: 节点对象
            source_handle: 源句柄
            
        Returns:
            匹配的输出键，如果没找到则返回None
        """
        for output in node.data.get("outputs", []):
            # 检查输出字段中是否有值等于source_handle的键
            for key, value in output.items():
                if value == source_handle:
                    return output.get("key")
        return None
    
    def _convert_labels_dict_to_list(self, labels):
        """
        将labels字典格式转换为数组格式
        
        Args:
            labels: 字典格式的labels，如 {key1: "value1", key2: "value2"}
            
        Returns:
            数组格式的labels，如 [{"key": key1, "value": "value1"}, {"key": key2, "value": "value2"}]
        """
        if isinstance(labels, dict):
            return [{"key": key, "value": value} for key, value in labels.items()]
        elif isinstance(labels, list):
            # 如果已经是数组格式，直接返回
            return labels
        else:
            # 其他情况返回空数组
            return []

    def _iter_label_items(self, raw_labels):
        """
        统一迭代标签声明为 (key, value) 形式，兼容多种声明方式。

        已实现且支持的输入格式：
        - dict：{k: v}，直接等价为 items()
        - list（仅处理元素为 dict 的情况）：
          1) {"key": k, "label": l, "valueType": vt}
          2) {"key": k, "valueType": vt}（label 默认等于 key）
          3) {k: {"label": l, "valueType": vt}}
          4) {k: "label"}（valueType 默认为 "string"）

        注意：
        - list 中非 dict 的元素会被忽略（例如 ["a", "b"] 不会被解析）。
        - 返回 list[tuple[key, value]]，其中 value 可能是 str 或 dict。
        """
        if isinstance(raw_labels, dict):
            return list(raw_labels.items())
        if isinstance(raw_labels, list):
            items = []
            for item in raw_labels:
                if not isinstance(item, dict):
                    continue
                if item.get("key") is not None:
                    items.append((item.get("key"), item))
                elif len(item) == 1:
                    k, v = next(iter(item.items()))
                    items.append((k, v))
            return items
        return []

    def _parse_codefragment_labels(self, config: Dict) -> Tuple[List[Dict], List[Dict]]:
        """
        解析 codeFragment 配置中的 input_labels / output_labels，构造参数型 inputs/outputs。

        注意：本方法会就地从 config 中弹出（pop）"input_labels" 与 "output_labels" 字段。

        入参与格式（示例）：
        - input_labels 可以是：
            {"title": "标题", "count": {"label": "数量", "valueType": "number"}}
          或：
            [{"key": "title", "label": "标题"}, {"key": "count", "valueType": "number"}]

        返回：
        - param_inputs: List[Dict]，形如
            {"connected": True, "valueType": "string", "description": "", "label": "标题", "type": "parameter", "key": "title"}
        - param_outputs: List[Dict]，形如
            {"valueType": "string", "description": "", "label": "标题", "type": "parameter", "targets": [], "key": "title"}
        """
        param_inputs: List[Dict] = []
        param_outputs: List[Dict] = []

        if "input_labels" in config:
            raw_in_labels = config.pop("input_labels", {})
            for key, value in self._iter_label_items(raw_in_labels):
                if key is None:
                    continue
                if isinstance(value, dict):
                    label_text = value.get("label", str(key))
                    value_type = value.get("valueType", "string")
                else:
                    label_text = str(value)
                    value_type = "string"
                param_inputs.append({
                    "connected": True,
                    "valueType": value_type,
                    "description": "",
                    "label": label_text,
                    "type": "parameter",
                    "key": key
                })

        if "output_labels" in config:
            raw_out_labels = config.pop("output_labels", {})
            for key, value in self._iter_label_items(raw_out_labels):
                if key is None:
                    continue
                if isinstance(value, dict):
                    label_text = value.get("label", str(key))
                    value_type = value.get("valueType", "string")
                else:
                    label_text = str(value)
                    value_type = "string"
                param_outputs.append({
                    "valueType": value_type,
                    "description": "",
                    "label": label_text,
                    "type": "parameter",
                    "targets": [],
                    "key": key
                })

        return param_inputs, param_outputs

    def compile(self,
                name: str = "未命名智能体", # 智能体名称
                avatar: str = "https://uat.agentspro.cn/assets/agent/avatar.png", # 头像URL
                intro: Optional[str] = None, # 智能体介绍
                chatAvatar: Optional[str] = None, # 对话头像URL
                shareAble: Optional[bool] = True, # 是否可分享
                guides: Optional[List] = None, # 引导配置
                category: Optional[str] = None, # 分类
                state: Optional[int] = None, # 状态
                prologue: Optional[str] = None, # 开场白
                extJsonObj: Optional[Dict] = None, # 扩展JSON对象
                allowVoiceInput: Optional[bool] = False, # 是否允许语音输入
                autoSendVoice: Optional[bool] = False, # 是否自动发送语音
                **kwargs) -> None: # 其他参数
        """
        编译并创建智能体应用
        """

        # 更新node里面的targets
        self._update_node()

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
        def get_field_type(node_id: str, field_key: str, field_category: str) -> Optional[str]:
            """
            从节点中查找字段类型
            
            Args:
                node_id: 节点ID
                field_key: 字段键名
                field_category: 字段类别 ('inputs' 或 'outputs')
            """
            for node in self.nodes:
                if node.id == node_id:
                    for field in node.data.get(field_category, []):
                        if field.get("key") == field_key:
                            return field.get("valueType")
                    break
            return None
        
        source_type = get_field_type(source, source_handle, "outputs")
        target_type = get_field_type(target, target_handle, "inputs")

        # 如果 source_type 或 target_type 为 "any"，则不需要检查类型一致性
        type_compatible = (source_type == "any" or target_type == "any") or (source_type == target_type)
        
        return (
            source_handle,
            target_handle if source_handle and target_handle and type_compatible else ""
        )
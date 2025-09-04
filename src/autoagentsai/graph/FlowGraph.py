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

    def set_start_node(self, position: dict = None, inputs: dict = None):
        """
        设置工作流的起始节点（questionInput类型）
        起始节点ID固定为"SimpleInputId"
        
        Args:
            position: 节点位置，默认为{"x": 0, "y": 300}
            inputs: 输入配置，默认为{"inputText": True, 其他为False}
        """
        if position is None:
            position = {"x": 0, "y": 300}
            
        # 默认配置：只启用文本输入
        default_inputs = {
            "inputText": True,
            "uploadFile": False,
            "uploadPicture": False,
            "fileContrast": False,
            "initialInput": True
        }
        
        # 如果用户提供了inputs，则合并配置
        if inputs:
            default_inputs.update(inputs)
        
        # 使用通用add_node方法添加起始节点
        self.add_node(
            node_id=self.START,
            module_type="questionInput",
            position=position,
            inputs=default_inputs
        )


    def add_memory_variables(self, node_id: str, position: dict = None, variables: dict = None):
        """
        添加记忆变量节点的简化方法
        
        Args:
            node_id: 节点ID
            position: 节点位置，默认为{"x": 0, "y": 1500}
            variables: 变量字典，格式为 {"key": "type"}，默认type为"string"
            
        Usage:
            graph.add_memory_variables("memory1", variables={
                "user_input": "string",
                "ai_response": "string",
                "file_content": "string"
            })
        """
        if position is None:
            position = {"x": 0, "y": 1500}
            
        if variables is None:
            variables = {}
            
        # 创建memory variable inputs
        memory_inputs = []
        for key, value_type in variables.items():
            if isinstance(value_type, str):
                # 如果只提供类型字符串，使用默认格式
                memory_inputs.append({
                    "key": key,
                    "value_type": value_type
                })
            else:
                # 如果提供完整对象，直接使用
                memory_inputs.append(value_type)
        
        # 使用通用add_node方法添加节点
        self.add_node(
            node_id=node_id,
            module_type="addMemoryVariable",
            position=position,
            inputs=memory_inputs
        )

    def add_node(self, node_id, module_type, position, inputs=None, outputs=None):
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
            
            # 转换简洁格式为展开格式
            converted_inputs = convert_json_to_json_list(inputs)
            converted_outputs = convert_json_to_json_list(outputs)
            final_inputs = merge_template_io(tpl.get("inputs", []), converted_inputs)
            final_outputs = merge_template_io(tpl.get("outputs", []), converted_outputs)

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

        return (
            source_handle,
            target_handle if source_handle and target_handle and source_type == target_type else ""
        )
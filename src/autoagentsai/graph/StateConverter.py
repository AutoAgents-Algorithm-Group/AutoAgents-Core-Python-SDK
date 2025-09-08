# src/autoagentsai/graph/StateConverter.py
from typing import Dict, Any, List, Optional, Union
from ..types.NodeStates import (
    BaseNodeState, HttpInvokeState, QuestionInputState, AiChatState,
    ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState
)


def state_to_module_type(state: BaseNodeState) -> str:
    """
    根据State类型推断module_type
    
    Args:
        state: 节点状态对象
        
    Returns:
        module_type字符串
        
    Raises:
        ValueError: 如果无法识别state类型
    """
    type_mapping = {
        HttpInvokeState: "httpInvoke",
        QuestionInputState: "questionInput", 
        AiChatState: "aiChat",
        ConfirmReplyState: "confirmreply",
        KnowledgeSearchState: "knowledgesSearch",
        Pdf2MdState: "pdf2md",
        AddMemoryVariableState: "addMemoryVariable",
        InfoClassState: "infoClass",
        CodeFragmentState: "codeFragment",
        ForEachState: "forEach",
    }
    
    for state_class, module_type in type_mapping.items():
        if isinstance(state, state_class):
            return module_type
            
    raise ValueError(f"Unknown state type: {type(state)}")


def state_to_inputs_outputs(state: BaseNodeState) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    从State对象转换为inputs和outputs配置
    
    Args:
        state: 节点状态对象
        
    Returns:
        tuple[inputs_dict, outputs_dict]: 输入和输出配置的元组
    """
    # 获取state的所有字段值
    state_dict = state.model_dump(exclude_none=True)
    
    # 提取基础字段（这些是inputs中的trigger相关字段）
    base_fields = {"switch", "switchAny", "finish"}
    inputs = {}
    outputs = {}
    
    # 根据不同的state类型进行特殊处理
    module_type = state_to_module_type(state)
    
    if module_type == "httpInvoke":
        # HTTP调用模块
        inputs.update({
            "url": state_dict.get("url", ""),
            "_requestBody_": state_dict.get("requestBody", "")
        })
        # outputs中的success/failed等由模板默认提供
        
    elif module_type == "questionInput":
        # 用户提问模块
        inputs.update({
            "inputText": state_dict.get("inputText", True),
            "uploadFile": state_dict.get("uploadFile", False),
            "uploadPicture": state_dict.get("uploadPicture", False),
            "fileUpload": state_dict.get("fileUpload", False),
            "fileContrast": state_dict.get("fileContrast", False),
            "fileInfo": state_dict.get("fileInfo", []),
            "initialInput": state_dict.get("initialInput", True)
        })
        
    elif module_type == "aiChat":
        # 智能对话模块
        inputs.update({
            "text": state_dict.get("text", ""),
            "images": state_dict.get("images", []),
            "knSearch": state_dict.get("knSearch", ""),
            "knConfig": state_dict.get("knConfig", ""),
            "historyText": state_dict.get("historyText", 3),
            "model": state_dict.get("model", "doubao-deepseek-v3"),
            "quotePrompt": state_dict.get("quotePrompt", ""),
            "stream": state_dict.get("stream", True),
            "temperature": state_dict.get("temperature", 0.0),
            "maxToken": state_dict.get("maxToken", 5000)
        })
        
    elif module_type == "confirmreply":
        # 确定回复模块
        inputs.update({
            "stream": state_dict.get("stream", True),
            "text": state_dict.get("text", "")
        })
        
    elif module_type == "knowledgesSearch":
        # 知识库搜索模块
        inputs.update({
            "text": state_dict.get("text", ""),
            "datasets": state_dict.get("datasets", []),
            "similarity": state_dict.get("similarity", 0.2),
            "vectorSimilarWeight": state_dict.get("vectorSimilarWeight", 1.0),
            "topK": state_dict.get("topK", 20),
            "enableRerank": state_dict.get("enableRerank", False),
            "rerankModelType": state_dict.get("rerankModelType", "oneapi-xinference:bce-rerank"),
            "rerankTopK": state_dict.get("rerankTopK", 10)
        })
        
    elif module_type == "pdf2md":
        # 通用文档解析模块
        inputs.update({
            "files": state_dict.get("files", []),
            "pdf2mdType": state_dict.get("pdf2mdType", "general")
        })
        
    elif module_type == "addMemoryVariable":
        # 添加记忆变量模块（特殊处理）
        variables = state_dict.get("variables", {})
        if variables:
            # 将variables字典转换为memory variable格式
            memory_inputs = []
            for key, value in variables.items():
                memory_inputs.append({
                    "key": key,
                    "value_type": "string"  # 默认类型
                })
            return memory_inputs, {}  # 特殊返回格式
        else:
            inputs.update({
                "feedback": state_dict.get("feedback", "")
            })
    
    elif module_type == "infoClass":
        # 信息分类模块
        inputs.update({
            "text": state_dict.get("text", ""),
            "knSearch": state_dict.get("knSearch", ""),
            "knConfig": state_dict.get("knConfig", ""),
            "historyText": state_dict.get("historyText", 3),
            "model": state_dict.get("model", "doubao-deepseek-v3"),
            "quotePrompt": state_dict.get("quotePrompt", ""),
            "labels": state_dict.get("labels", {})
        })
        
    elif module_type == "codeFragment":
        # 代码块模块
        inputs.update({
            "_language_": state_dict.get("language", "js"),
            "_description_": state_dict.get("description", ""),
            "_code_": state_dict.get("code", "")
        })
        # 如果有动态inputs/outputs，也需要处理
        if state_dict.get("inputs"):
            inputs.update(state_dict["inputs"])
        if state_dict.get("outputs"):
            outputs.update(state_dict["outputs"])
            
    elif module_type == "forEach":
        # 循环模块
        inputs.update({
            "items": state_dict.get("items", []),
            "index": state_dict.get("index", 0),
            "item": state_dict.get("item"),
            "length": state_dict.get("length", 0),
            "loopEnd": state_dict.get("loopEnd", False)
        })
    
    return inputs, outputs


def create_node_from_state(
    state: BaseNodeState,
    node_id: str,
    position: Dict[str, float]
) -> tuple[str, str, Dict[str, float], Dict[str, Any], Dict[str, Any]]:
    """
    从State对象创建节点所需的所有参数
    
    Args:
        state: 节点状态对象
        node_id: 节点ID
        position: 节点位置
        
    Returns:
        tuple[node_id, module_type, position, inputs, outputs]
    """
    module_type = state_to_module_type(state)
    inputs, outputs = state_to_inputs_outputs(state)
    
    return node_id, module_type, position, inputs, outputs

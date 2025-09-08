# src/autoagentsai/dify/DifyTypes.py
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


class FileUploadConfig(BaseModel):
    """文件上传配置"""
    audio_file_size_limit: Optional[int] = 50
    batch_count_limit: Optional[int] = 5
    file_size_limit: Optional[int] = 15
    image_file_size_limit: Optional[int] = 10
    video_file_size_limit: Optional[int] = 100
    workflow_file_upload_limit: Optional[int] = 10


class ImageConfig(BaseModel):
    """图片配置"""
    enabled: Optional[bool] = False
    number_limits: Optional[int] = 3
    transfer_methods: Optional[List[str]] = Field(default_factory=lambda: ["local_file", "remote_url"])


class FileUpload(BaseModel):
    """文件上传功能配置"""
    allowed_file_extensions: Optional[List[str]] = Field(default_factory=list)
    allowed_file_types: Optional[List[str]] = Field(default_factory=list)
    allowed_file_upload_methods: Optional[List[str]] = Field(default_factory=lambda: ["local_file", "remote_url"])
    enabled: Optional[bool] = False
    fileUploadConfig: Optional[FileUploadConfig] = None
    image: Optional[ImageConfig] = None
    number_limits: Optional[int] = 3


class WorkflowFeatures(BaseModel):
    """工作流功能配置"""
    file_upload: Optional[FileUpload] = None
    opening_statement: Optional[str] = ""
    retriever_resource: Optional[Dict[str, bool]] = Field(default_factory=lambda: {"enabled": True})
    sensitive_word_avoidance: Optional[Dict[str, bool]] = Field(default_factory=lambda: {"enabled": False})
    speech_to_text: Optional[Dict[str, bool]] = Field(default_factory=lambda: {"enabled": False})
    suggested_questions: Optional[List[str]] = Field(default_factory=list)
    suggested_questions_after_answer: Optional[Dict[str, bool]] = Field(default_factory=lambda: {"enabled": False})
    text_to_speech: Optional[Dict[str, Any]] = Field(default_factory=lambda: {"enabled": False, "language": "", "voice": ""})


class Position(BaseModel):
    """位置坐标"""
    x: float
    y: float


class Viewport(BaseModel):
    """视口配置"""
    x: float
    y: float
    zoom: float


class EdgeData(BaseModel):
    """边数据"""
    isInLoop: Optional[bool] = False
    sourceType: Optional[str] = ""
    targetType: Optional[str] = ""


class DifyEdge(BaseModel):
    """Dify边定义"""
    data: Optional[EdgeData] = None
    id: str
    source: str
    sourceHandle: Optional[str] = "source"
    target: str
    targetHandle: Optional[str] = "target"
    type: Optional[str] = "custom"
    zIndex: Optional[int] = 0


class ModelConfig(BaseModel):
    """模型配置"""
    mode: Optional[str] = "chat"
    name: Optional[str] = ""
    provider: Optional[str] = ""
    completion_params: Optional[Dict[str, Any]] = Field(default_factory=lambda: {"temperature": 0.7})


class PromptTemplate(BaseModel):
    """提示词模板"""
    role: str
    text: str


class ContextConfig(BaseModel):
    """上下文配置"""
    enabled: Optional[bool] = False
    variable_selector: Optional[List[str]] = Field(default_factory=list)


class VisionConfig(BaseModel):
    """视觉配置"""
    enabled: Optional[bool] = False


class RetrievalConfig(BaseModel):
    """检索配置"""
    top_k: Optional[int] = 4
    reranking_enable: Optional[bool] = False


class Authorization(BaseModel):
    """授权配置"""
    type: Optional[str] = "no-auth"


class RequestBody(BaseModel):
    """请求体配置"""
    type: Optional[str] = "none"


class NodeData(BaseModel):
    """节点数据基类"""
    type: str
    title: str
    desc: Optional[str] = ""
    selected: Optional[bool] = False


class StartNodeData(NodeData):
    """开始节点数据"""
    variables: Optional[List[str]] = Field(default_factory=list)


class LLMNodeData(NodeData):
    """LLM节点数据"""
    model: Optional[ModelConfig] = None
    prompt_template: Optional[List[PromptTemplate]] = Field(default_factory=list)
    context: Optional[ContextConfig] = None
    vision: Optional[VisionConfig] = None
    variables: Optional[List[str]] = Field(default_factory=list)


class KnowledgeRetrievalNodeData(NodeData):
    """知识检索节点数据"""
    dataset_ids: Optional[List[str]] = Field(default_factory=list)
    query_variable_selector: Optional[List[str]] = Field(default_factory=list)
    retrieval_mode: Optional[str] = "multiple"
    multiple_retrieval_config: Optional[RetrievalConfig] = None


class EndNodeData(NodeData):
    """结束节点数据"""
    outputs: Optional[List[str]] = Field(default_factory=list)


class IfElseNodeData(NodeData):
    """条件分支节点数据"""
    conditions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    logical_operator: Optional[str] = "and"


class CodeNodeData(NodeData):
    """代码执行节点数据"""
    code: Optional[str] = ""
    code_language: Optional[str] = "python3"
    variables: Optional[List[str]] = Field(default_factory=list)
    outputs: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TemplateTransformNodeData(NodeData):
    """模板转换节点数据"""
    template: Optional[str] = ""
    variables: Optional[List[str]] = Field(default_factory=list)


class QuestionClassifierNodeData(NodeData):
    """问题分类器节点数据"""
    query_variable_selector: Optional[List[str]] = Field(default_factory=list)
    topics: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    model: Optional[ModelConfig] = None


class HttpRequestNodeData(NodeData):
    """HTTP请求节点数据"""
    method: Optional[str] = "get"
    url: Optional[str] = ""
    authorization: Optional[Authorization] = None
    headers: Optional[str] = ""
    params: Optional[str] = ""
    body: Optional[RequestBody] = None


class VariableAggregatorNodeData(NodeData):
    """变量聚合器节点数据"""
    variables: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class DifyNode(BaseModel):
    """Dify节点定义"""
    data: Union[
        StartNodeData, LLMNodeData, KnowledgeRetrievalNodeData, EndNodeData,
        IfElseNodeData, CodeNodeData, TemplateTransformNodeData,
        QuestionClassifierNodeData, HttpRequestNodeData, VariableAggregatorNodeData
    ]
    height: Optional[int] = 54
    id: str
    position: Position
    positionAbsolute: Optional[Position] = None
    selected: Optional[bool] = False
    sourcePosition: Optional[str] = "right"
    targetPosition: Optional[str] = "left"
    type: Optional[str] = "custom"
    width: Optional[int] = 244


class DifyGraphModel(BaseModel):
    """Dify图配置"""
    edges: List[DifyEdge] = Field(default_factory=list)
    nodes: List[DifyNode] = Field(default_factory=list)
    viewport: Optional[Viewport] = None


class DifyWorkflow(BaseModel):
    """Dify工作流配置"""
    conversation_variables: Optional[List[str]] = Field(default_factory=list)
    environment_variables: Optional[List[str]] = Field(default_factory=list)
    features: Optional[WorkflowFeatures] = None
    graph: Optional[DifyGraphModel] = None


class DifyApp(BaseModel):
    """Dify应用配置"""
    description: Optional[str] = ""
    icon: Optional[str] = "🤖"
    icon_background: Optional[str] = "#FFEAD5"
    mode: Optional[str] = "workflow"
    name: Optional[str] = ""
    use_icon_as_answer_icon: Optional[bool] = False


class DifyConfig(BaseModel):
    """完整的Dify配置"""
    app: Optional[DifyApp] = None
    dependencies: Optional[List[str]] = Field(default_factory=list)
    kind: Optional[str] = "app"
    version: Optional[str] = "0.3.1"
    workflow: Optional[DifyWorkflow] = None


# 节点数据工厂字典
NODE_DATA_FACTORY = {
    "start": StartNodeData,
    "llm": LLMNodeData,
    "knowledge-retrieval": KnowledgeRetrievalNodeData,
    "end": EndNodeData,
    "if-else": IfElseNodeData,
    "code": CodeNodeData,
    "template-transform": TemplateTransformNodeData,
    "question-classifier": QuestionClassifierNodeData,
    "http-request": HttpRequestNodeData,
    "variable-aggregator": VariableAggregatorNodeData,
}


def create_node_data(node_type: str, **kwargs) -> NodeData:
    """
    根据节点类型创建对应的NodeData实例
    
    Args:
        node_type: 节点类型
        **kwargs: 初始化参数
        
    Returns:
        对应的NodeData实例
        
    Raises:
        ValueError: 当node_type不支持时
    """
    data_class = NODE_DATA_FACTORY.get(node_type)
    if not data_class:
        raise ValueError(f"Unsupported node_type: {node_type}")
    
    # 确保type字段正确设置
    kwargs["type"] = node_type
    return data_class(**kwargs)

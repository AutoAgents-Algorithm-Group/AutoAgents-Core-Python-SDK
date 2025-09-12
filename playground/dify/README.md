# DifyGraph 和 Text2Workflow 使用指南

本目录包含了针对 Dify 平台的工作流构建工具以及统一的 Text2Workflow 接口。

## 功能特性

### 🎯 DifyGraph
- **类似 FlowGraph 的 API**: 与现有的 AgentsPro FlowGraph 保持相似的接口设计
- **原生 Dify 支持**: 直接生成符合 Dify 平台标准的 YAML 配置文件
- **节点类型支持**: start、llm、knowledge-retrieval、end 等核心节点类型
- **YAML 导入导出**: 支持从现有 YAML 文件加载并修改工作流

### 🔄 Text2Workflow (简化版)
- **多平台统一接口**: 一套 API 同时支持 `dify` 和 `agentify` 两个平台
- **平台自动适配**: 根据指定平台自动调用对应的底层实现
- **简化的 API**: **只需要一个 `add_node` 方法，通过 BaseModel 自动判断节点类型**
- **智能类型推断**: 支持 Dify 原生数据和 AgentsPro State 的混合使用
- **自动转换**: AgentsPro State 自动转换为 Dify 格式

## 快速开始

### 1. 使用 DifyGraph

```python
from autoagentsai.dify import DifyGraph

# 创建图实例
graph = DifyGraph(
    app_name="智能助手",
    app_description="基于 Dify 的智能工作流",
    app_icon="🤖"
)

# 添加节点
graph.add_node("start", "start", {"x": 50, "y": 200})
graph.add_node("llm1", "llm", {"x": 300, "y": 200}, 
               title="AI对话",
               prompt_template=[{"role": "system", "text": "你是一个智能助手"}])
graph.add_node("end", "end", {"x": 550, "y": 200})

# 添加连接
graph.add_edge("start", "llm1")
graph.add_edge("llm1", "end")

# 导出为 YAML
graph.save_yaml("my_workflow.yaml")
```

### 2. 使用 Text2Workflow (简化版 API) - Dify 平台

```python
from autoagentsai.graph import Text2Workflow
from autoagentsai.types.GraphTypes import AiChatState
from autoagentsai.dify.DifyTypes import DifyStartNodeData, DifyLLMNodeData

# 创建 Dify 平台工作流
workflow = Text2Workflow(platform="dify", app_name="智能助手")

# 方式1: 使用 Dify 原生数据
start_data = DifyStartNodeData(title="开始")
workflow.add_node("start", start_data, {"x": 50, "y": 200})

llm_data = DifyLLMNodeData(
    title="AI助手",
    prompt_template=[{"role": "system", "text": "你是专业助手"}],
    model={"name": "doubao-deepseek-v3", "completion_params": {"temperature": 0.7}}
)
workflow.add_node("chat", llm_data, {"x": 300, "y": 200})

# 方式2: 使用 AgentsPro State（自动转换为 Dify 格式）
ai_state = AiChatState(
    model="doubao-deepseek-v3",
    text="你是专业的客服人员",
    temperature=0.7
)
workflow.add_node("ai_converted", ai_state, {"x": 550, "y": 200})

# 连接和编译
workflow.add_edge("start", "chat")
workflow.add_edge("chat", "ai_converted")
yaml_output = workflow.compile()
```

### 3. 使用 Text2Workflow (简化版 API) - AgentsPro 平台

```python
from autoagentsai.graph import Text2Workflow
from autoagentsai.types.GraphTypes import QuestionInputState, AiChatState, ConfirmReplyState

# 创建 AgentsPro 平台工作流
workflow = Text2Workflow(
    platform="agentify",
    personal_auth_key="your_auth_key",
    personal_auth_secret="your_auth_secret"
)

# 使用 AgentsPro 原生 State
input_state = QuestionInputState(inputText=True, uploadFile=True)
workflow.add_node("input", input_state, {"x": 50, "y": 200})

ai_state = AiChatState(model="doubao-deepseek-v3", text="你好！", temperature=0.7)
workflow.add_node("ai", ai_state, {"x": 300, "y": 200})

reply_state = ConfirmReplyState(text="感谢使用！")
workflow.add_node("reply", reply_state, {"x": 550, "y": 200})

# 连接和编译
workflow.add_edge("input", "ai")
workflow.add_edge("ai", "reply")
workflow.compile(name="我的智能体")  # 直接发布到平台
```

## 支持的 BaseModel 类型

### Dify 原生 NodeData
- **DifyStartNodeData**: 开始节点数据
- **DifyLLMNodeData**: 大语言模型节点数据
- **DifyKnowledgeRetrievalNodeData**: 知识检索节点数据
- **DifyEndNodeData**: 结束节点数据

### AgentsPro State (自动转换)
- **QuestionInputState** → `start` 节点
- **AiChatState** → `llm` 节点
- **KnowledgeSearchState** → `knowledge-retrieval` 节点
- **ConfirmReplyState** → `end` 节点
- **HttpInvokeState** → 自定义节点
- **其他 State** → 对应的节点类型

## 文件说明

- `dify.yaml`: 原始的 Dify 工作流配置文件
- `test_dify.py`: **DifyGraph 和 Text2Workflow 的完整测试用例**
- `README.md`: 本说明文档

### 其他测试文件
- `../graph/test_text2workflow.py`: **Text2Workflow 在 graph 目录中的标准测试**


## 高级功能

### 从现有 YAML 加载

```python
# 从文件加载
graph = DifyGraph.from_yaml_file("existing_workflow.yaml")

# 修改配置
graph.app.name = "修改后的工作流"
graph.add_node("new_node", "llm", {"x": 800, "y": 200})

# 重新保存
graph.save_yaml("modified_workflow.yaml")
```

### 平台切换

```python
# 创建 Dify 版本
dify_workflow = Text2Workflow(platform="dify")

# 创建 AgentsPro 版本（相同的 API）
agentify_workflow = Text2Workflow(
    platform="agentify",
    personal_auth_key="...",
    personal_auth_secret="..."
)
```

## 🚀 简化 API 的优势

### 1. **统一接口**
只需要一个 `add_node` 方法，不需要记忆多个特定方法：
```python
# ❌ 旧方式：需要多个方法
workflow.add_start_node("start")
workflow.add_ai_chat_node("chat", model="...", prompt="...")
workflow.add_knowledge_search_node("search", datasets=[...])
workflow.add_end_node("end")

# ✅ 新方式：统一方法
workflow.add_node("start", start_state, position)
workflow.add_node("chat", ai_state, position)
workflow.add_node("search", knowledge_state, position)
workflow.add_node("end", end_state, position)
```

### 2. **类型安全**
通过 BaseModel 获得更好的类型检查和 IDE 支持：
```python
from autoagentsai.types.GraphTypes import AiChatState

# 类型安全的状态定义
ai_state = AiChatState(
    model="doubao-deepseek-v3",
    temperature=0.7,
    text="你是专业助手"
)
workflow.add_node("ai", ai_state, {"x": 300, "y": 200})
```

### 3. **平台无关**
相同的代码可以在不同平台间切换：
```python
# 只需要改变 platform 参数
dify_workflow = Text2Workflow(platform="dify")
agentify_workflow = Text2Workflow(platform="agentify", auth_key="...", auth_secret="...")

# 相同的节点添加代码
for workflow in [dify_workflow, agentify_workflow]:
    workflow.add_node("ai", ai_state, position)
```

### 4. **混合使用**
在同一个工作流中混合使用不同类型的 BaseModel：
```python
# Dify 原生数据
start_data = DifyStartNodeData(title="开始")
workflow.add_node("start", start_data, position)

# AgentsPro State（自动转换）
ai_state = AiChatState(model="doubao-deepseek-v3", text="Hello")
workflow.add_node("ai", ai_state, position)
```

## 注意事项

1. **认证信息**: AgentsPro 平台需要有效的 `personal_auth_key` 和 `personal_auth_secret`
2. **模型选择**: 默认使用 `doubao-deepseek-v3` 模型，可根据需要调整
3. **YAML 格式**: 生成的 YAML 文件完全符合 Dify 平台标准
4. **节点位置**: 建议合理设置节点位置以获得更好的视觉效果
5. **BaseModel**: 确保传入的 state 参数是有效的 BaseModel 实例

## 运行测试

```bash
# 在 dify 目录中运行
cd playground/dify
python test_dify.py

# 在 graph 目录中运行 Text2Workflow 标准测试
cd playground/graph
python test_text2workflow.py
```

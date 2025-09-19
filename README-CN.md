<div align="center">

<img src="https://img.shields.io/badge/-autoagents_core%20Python%20SDK-000000?style=for-the-badge&labelColor=faf9f6&color=faf9f6&logoColor=000000" alt="autoagents_core Python SDK" width="380"/>

<h4>企业级AI智能体搭建平台 Python SDK</h4>

[English](README.md) | 简体中文



<a href="https://pypi.org/project/autoagents-core">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/pypi/v/autoagents-core.svg?style=for-the-badge" />
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/autoagents-core.svg?style=for-the-badge" />
  </picture>
</a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="media/dark_license.svg" />
  <img alt="License MIT" src="media/light_license.svg" />
</picture>

</div>

专业的 AutoAgents AI 平台 Python SDK，为智能对话、文件处理、知识库管理等功能提供直观易用的 API 接口。

## 目录
- [为什么选择 AutoAgents Core Python SDK？](#为什么选择-autoagents-core-python-sdk)
- [快速开始](#快速开始)
- [核心特性](#核心特性)
- [示例](#示例)
- [贡献](#贡献)
- [许可证](#许可证)

## 为什么选择 AutoAgents Core Python SDK？

AutoAgents Core AI Python SDK 是一个综合性工具包，改变了开发人员与 AI 驱动的自动化系统交互的方式。专为现代 Python 应用程序构建，提供与 AutoAgents AI 平台的无缝集成。

### 核心特性

#### 智能对话
- **流式对话**：实时对话，支持多轮交互
- **推理过程**：显示 AI 思考和决策步骤
- **多模态支持**：在统一接口中处理文本、图片和文件

#### 文件处理
- **多格式支持**：自动处理 PDF、Word、图片等多种格式
- **智能分析**：从文档中提取洞察和内容
- **批量操作**：高效处理多个文件

#### 知识库管理
- **完整的 CRUD 操作**：创建、读取、更新、删除知识库
- **高级搜索**：语义搜索和内容检索
- **内容组织**：结构化存储和管理

#### 预构建智能体
- **PowerPoint 生成**：从模板和数据创建演示文稿
- **React 智能体**：交互式问题解决智能体
- **工作流自动化**：复杂的多步骤任务编排
- **数据科学工具**：分析和可视化功能

#### 现代架构
- **异步支持**：高性能异步 API 调用
- **类型安全**：完整的 Pydantic 类型验证
- **可扩展设计**：用于自定义解决方案的模块化组件

### 为什么选择 AutoAgents Core AI Python SDK？

- **开发者优先**：为现代 Python 开发设计的直观 API
- **生产就绪**：在企业环境中经过实战测试
- **功能全面**：一个包中包含 AI 自动化所需的一切
- **文档完善**：丰富的示例和清晰的 API 文档

## 快速开始

### 前提条件
- Python 3.11+
- AutoAgents AI 平台账户

### 安装

```bash
pip install autoagents-core
```


### 获取 API 密钥

1. 登录 AutoAgents AI 平台
2. 导航到 个人资料 → 个人密钥
3. 复制您的 `personal_auth_key` 和 `personal_auth_secret`

### 第一次对话

```python
from autoagents_core.client import ChatClient

# 初始化客户端
client = ChatClient(
    agent_id="your_agent_id",
    personal_auth_key="your_auth_key", 
    personal_auth_secret="your_auth_secret"
)

# 开始对话
for event in client.invoke("你好，请介绍一下人工智能"):
    if event['type'] == 'token':
        print(event['content'], end='', flush=True)
    elif event['type'] == 'finish':
        break
```

### 文件处理

```python
# 上传并分析文件
for event in client.invoke(
    prompt="请分析这个文档的主要内容",
    files=["document.pdf"]
):
    if event['type'] == 'token':
        print(event['content'], end='', flush=True)
```

### 知识库管理

```python
from autoagents_core.client import KbClient

# 初始化知识库客户端
kb_client = KbClient(
    personal_auth_key="your_auth_key",
    personal_auth_secret="your_auth_secret"
)

# 创建知识库
result = kb_client.create_kb(
    name="技术文档库",
    description="存储技术相关文档"
)

# 查询知识库列表
kb_list = kb_client.query_kb_list()
```

### 幻灯片生成

```python
from autoagents_core.slide import SlideAgent

# 创建幻灯片智能体
slide_agent = SlideAgent()

# 生成演示文稿
slide_agent.fill(
    prompt="创建一个关于 AI 发展的演示文稿",
    template_file_path="template.pptx",
    output_file_path="output.pptx"
)
```

### 高级工作流自动化

```python
from autoagents_core.graph import FlowGraph

# 创建工作流图
graph = FlowGraph(
    personal_auth_key="your_auth_key",
    personal_auth_secret="your_auth_secret"
)

# 添加工作流节点并编译
graph.add_node("chat_node", "chat", {"prompt": "分析这些数据"})
graph.add_node("ppt_node", "slide", {"template": "report.pptx"})
graph.add_edge("chat_node", "ppt_node")

# 部署工作流
graph.compile(workflow_name="数据分析流水线")
```


### 获取 Agent ID

1. 打开 Agent 详情页面
2. 点击 "分享" → "API"
3. 复制 Agent ID

## 示例

浏览 `playground/` 目录获取全面的示例：

- `playground/client/` - 对话和 API 示例
- `playground/slide/` - PowerPoint 生成示例
- `playground/kb/` - 知识库管理
- `playground/react/` - React Agent 示例
- `playground/datascience/` - 数据分析工具

## 贡献

我们欢迎贡献！请随时提交问题和拉取请求。

### 开发环境设置

```bash
git clone https://github.com/your-repo/autoagents-core-python-sdk.git
cd autoagents_core-python-sdk
pip install -e .[dev]
```

## 许可证

MIT License

<div align="center">

<img src="https://img.shields.io/badge/-autoagents_core-000000?style=for-the-badge&labelColor=faf9f6&color=faf9f6&logoColor=000000" alt="autoagents_core Python SDK" width="380"/>

<h4>Enterprise-level AI Agent Building Platform Python SDK</h4>

English | [简体中文](README-CN.md)



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

Professional Python SDK for AutoAgents AI platform, providing intuitive APIs for intelligent conversation, file processing, knowledge base management, and more.

## Table of Contents
- [Why AutoAgents Core Python SDK?](#why-autoagents-core-python-sdk)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Why AutoAgents Core Python SDK?

AutoAgents Core AI Python SDK is a comprehensive toolkit that transforms how developers interact with AI-powered automation systems. Built for modern Python applications, it provides seamless integration with the AutoAgents AI platform.

### Core Features

#### Intelligent Conversation
- **Streaming Chat**: Real-time conversation with multi-turn interactions
- **Reasoning Process**: Display AI thinking and decision-making steps
- **Multi-modal Support**: Handle text, images, and files in unified interface

#### File Processing
- **Multi-format Support**: Automatic processing of PDF, Word, images, and more
- **Smart Analysis**: Extract insights and content from documents
- **Batch Operations**: Handle multiple files efficiently

#### Knowledge Base Management
- **Complete CRUD Operations**: Create, read, update, delete knowledge bases
- **Advanced Search**: Semantic search and content retrieval
- **Content Organization**: Structured storage and management

#### Pre-built Agents
- **PowerPoint Generation**: Create presentations from templates and data
- **React Agents**: Interactive problem-solving agents
- **Workflow Automation**: Complex multi-step task orchestration
- **Data Science Tools**: Analytics and visualization capabilities

#### Modern Architecture
- **Async Support**: High-performance asynchronous API calls
- **Type Safety**: Full Pydantic type validation
- **Extensible Design**: Modular components for custom solutions

### Why Choose AutoAgents Core AI Python SDK?

- **Developer-First**: Intuitive APIs designed for modern Python development
- **Production-Ready**: Battle-tested in enterprise environments
- **Comprehensive**: Everything needed for AI automation in one package
- **Well-Documented**: Extensive examples and clear API documentation

## Quick Start

### Prerequisites
- Python 3.11+
- AutoAgents AI platform account

### Installation

```bash
pip install autoagents-core
```

### Get API Keys

1. Log in to AutoAgents AI platform
2. Navigate to Profile → Personal Keys
3. Copy your `personal_auth_key` and `personal_auth_secret`

### First Conversation

```python
from autoagents_core.client import ChatClient

# Initialize client
client = ChatClient(
    agent_id="your_agent_id",
    personal_auth_key="your_auth_key", 
    personal_auth_secret="your_auth_secret"
)

# Start conversation
for event in client.invoke("Hello, please introduce artificial intelligence"):
    if event['type'] == 'token':
        print(event['content'], end='', flush=True)
    elif event['type'] == 'finish':
        break
```

### File Processing

```python
# Upload and analyze files
for event in client.invoke(
    prompt="Please analyze the main content of this document",
    files=["document.pdf"]
):
    if event['type'] == 'token':
        print(event['content'], end='', flush=True)
```

### Knowledge Base Management

```python
from autoagents_core.client import KbClient

# Initialize knowledge base client
kb_client = KbClient(
    personal_auth_key="your_auth_key",
    personal_auth_secret="your_auth_secret"
)

# Create knowledge base
result = kb_client.create_kb(
    name="Technical Documentation",
    description="Store technical documents"
)

# Query knowledge base list
kb_list = kb_client.query_kb_list()
```

### Slide Generation

```python
from autoagents_core.slide import SlideAgent

# Create slide agent
slide_agent = SlideAgent()

# Generate presentation
slide_agent.fill(
    prompt="Create a presentation about AI development",
    template_file_path="template.pptx",
    output_file_path="output.pptx"
)
```

### Advanced Workflow Automation

```python
from autoagents_core.graph import FlowGraph

# Create workflow graph
graph = FlowGraph(
    personal_auth_key="your_auth_key",
    personal_auth_secret="your_auth_secret"
)

# Add workflow nodes and compile
graph.add_node("chat_node", "chat", {"prompt": "Analyze this data"})
graph.add_node("ppt_node", "slide", {"template": "report.pptx"})
graph.add_edge("chat_node", "ppt_node")

# Deploy workflow
graph.compile(workflow_name="data_analysis_pipeline")
```


### Getting Agent ID

1. Open Agent details page
2. Click "Share" → "API"
3. Copy Agent ID

## Examples

Explore the `playground/` directory for comprehensive examples:

- `playground/client/` - Chat and API examples
- `playground/slide/` - PowerPoint generation examples
- `playground/kb/` - Knowledge base management
- `playground/react/` - React Agent examples
- `playground/datascience/` - Data analysis tools

## Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

### Development Setup

```bash
git clone https://github.com/your-repo/autoagents-core-python-sdk.git
cd autoagents_core-python-sdk
pip install -e .[dev]
```

## License

MIT License


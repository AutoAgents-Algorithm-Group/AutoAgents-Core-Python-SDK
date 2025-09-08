# src/autoagentsai/__init__.py
from .client import ChatClient, KbClient, CrawlClient, SupabaseClient, MCPClient
from .graph import FlowGraph, FlowInterpreter, AutoWorkFlow
from .datascience import DSAgent
from .react import ReActAgent
from .sandbox import LocalSandbox, E2BSandbox
from .slide import SlideAgent
from .publish import Publisher
from .tools import ToolManager
from .types import *
from .dify import DifyGraph

__all__ = [
    "ChatClient", "KbClient", "CrawlClient", "SupabaseClient", "MCPClient",
    "FlowGraph", "FlowInterpreter", "AutoWorkFlow",
    "DSAgent", 
    "ReActAgent",
    "LocalSandbox", "E2BSandbox",
    "SlideAgent",
    "Publisher",
    "ToolManager",
    "DifyGraph"
]


def main() -> None:
    print("Hello from autoagents-python-sdk!")
# src/autoagents_core/__init__.py
from .client import ChatClient, KbClient, CrawlClient, SupabaseClient, MCPClient
from .datascience import DSAgent
from .react import ReActAgent
from .sandbox import LocalSandbox, E2BSandbox
from .slide import SlideAgent
from .publish import Publisher
from .tools import ToolManager
from .types import *

__all__ = [
    "ChatClient", "KbClient", "CrawlClient", "SupabaseClient", "MCPClient",
    "DSAgent", 
    "ReActAgent",
    "LocalSandbox", "E2BSandbox",
    "SlideAgent",
    "Publisher",
    "ToolManager",
]


def main() -> None:
    print("Hello from autoagents_core-python-sdk!")
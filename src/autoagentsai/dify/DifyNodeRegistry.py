# src/autoagentsai/dify/DifyNodeRegistry.py
from typing import Dict, Any, List

DIFY_NODE_TEMPLATES = {
    "start": {
        "type": "start",
        "title": "开始",
        "desc": "",
        "data": {
            "type": "start",
            "title": "开始",
            "desc": "",
            "selected": False,
            "variables": []
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "llm": {
        "type": "llm", 
        "title": "LLM",
        "desc": "",
        "data": {
            "type": "llm",
            "title": "LLM",
            "desc": "",
            "selected": False,
            "model": {
                "mode": "chat",
                "name": "",
                "provider": "",
                "completion_params": {
                    "temperature": 0.7
                }
            },
            "prompt_template": [
                {
                    "role": "system",
                    "text": ""
                }
            ],
            "context": {
                "enabled": False,
                "variable_selector": []
            },
            "vision": {
                "enabled": False
            },
            "variables": []
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "knowledge-retrieval": {
        "type": "knowledge-retrieval",
        "title": "知识检索",
        "desc": "",
        "data": {
            "type": "knowledge-retrieval",
            "title": "知识检索",
            "desc": "",
            "selected": False,
            "dataset_ids": [],
            "query_variable_selector": [],
            "retrieval_mode": "multiple",
            "multiple_retrieval_config": {
                "top_k": 4,
                "reranking_enable": False
            }
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "end": {
        "type": "end",
        "title": "结束", 
        "desc": "",
        "data": {
            "type": "end",
            "title": "结束",
            "desc": "",
            "selected": False,
            "outputs": []
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "if-else": {
        "type": "if-else",
        "title": "条件分支",
        "desc": "",
        "data": {
            "type": "if-else", 
            "title": "条件分支",
            "desc": "",
            "selected": False,
            "conditions": [],
            "logical_operator": "and"
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "code": {
        "type": "code",
        "title": "代码执行",
        "desc": "",
        "data": {
            "type": "code",
            "title": "代码执行", 
            "desc": "",
            "selected": False,
            "code": "",
            "code_language": "python3",
            "variables": [],
            "outputs": {}
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "template-transform": {
        "type": "template-transform",
        "title": "模板转换",
        "desc": "",
        "data": {
            "type": "template-transform",
            "title": "模板转换",
            "desc": "",
            "selected": False,
            "template": "",
            "variables": []
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "question-classifier": {
        "type": "question-classifier",
        "title": "问题分类器",
        "desc": "",
        "data": {
            "type": "question-classifier",
            "title": "问题分类器",
            "desc": "",
            "selected": False,
            "query_variable_selector": [],
            "topics": [],
            "model": {
                "mode": "chat",
                "name": "",
                "provider": "",
                "completion_params": {
                    "temperature": 0.7
                }
            }
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "http-request": {
        "type": "http-request",
        "title": "HTTP请求",
        "desc": "",
        "data": {
            "type": "http-request",
            "title": "HTTP请求",
            "desc": "",
            "selected": False,
            "method": "get",
            "url": "",
            "authorization": {
                "type": "no-auth"
            },
            "headers": "",
            "params": "",
            "body": {
                "type": "none"
            }
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    },
    "variable-aggregator": {
        "type": "variable-aggregator",
        "title": "变量聚合器",
        "desc": "",
        "data": {
            "type": "variable-aggregator",
            "title": "变量聚合器",
            "desc": "",
            "selected": False,
            "variables": []
        },
        "width": 244,
        "height": 54,
        "sourcePosition": "right",
        "targetPosition": "left"
    }
}


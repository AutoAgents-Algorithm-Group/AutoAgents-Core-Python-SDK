from autoagentsai.graph import FlowGraph


def main():
    graph = FlowGraph(
            personal_auth_key="7217394b7d3e4becab017447adeac239",
            personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
            base_url="https://uat.agentspro.cn"
        )

    # 添加节点
    graph.add_node(
        node_id="simpleInputId",
        module_type="questionInput",
        position={'x': 0, 'y': 300},
        inputs={
            "inputText": True,
            "uploadFile": True,
            "uploadPicture": False,
            "fileUpload": False,
            "fileContrast": False,
            "fileInfo": [],
            "initialInput": True,
        }
    )

    graph.add_node(
        node_id="pdf2md1",
        module_type="pdf2md",
        position={'x': 500, 'y': 300},
        inputs={
            "files": "",
            "pdf2mdType": "deep_pdf2md",
        }
    )

    graph.add_node(
        node_id="confirmreply1",
        module_type="confirmreply",
        position={'x': 1000, 'y': 300},
        inputs={
            "stream": True,
            "text": "文件内容：{{@pdf2md1_pdf2mdResult}}",
        }
    )

    graph.add_node(
        node_id="ai1",
        module_type="aiChat",
        position={'x': 1500, 'y': 300},
        inputs={
            "text": "",
            "images": "",
            "knSearch": "",
            "historyText": 3,
            "model": "doubao-deepseek-v3",
            "quotePrompt": """
<角色>
你是一个文件解答助手，你可以根据文件内容，解答用户的问题
</角色>

<文件内容>
{{@pdf2md1_pdf2mdResult}}
</文件内容>

<用户问题>
{{@question1_userChatInput}}
</用户问题>
            """,
            "stream": True,
            "temperature": 0.1,
            "topP": 1,
            "maxToken": 5000,
        }
    )

    memory_variable_inputs = []
    question1_userChatInput = {
        "key": "question1_userChatInput",
        "value_type": "string"
    }
    memory_variable_inputs.append(question1_userChatInput)
    pdf2md1_pdf2mdResult = {
        "key": "pdf2md1_pdf2mdResult",
        "value_type": "string"
    }
    memory_variable_inputs.append(pdf2md1_pdf2mdResult)
    ai1_answerText = {
        "key": "ai1_answerText",
        "value_type": "string"
    }
    memory_variable_inputs.append(ai1_answerText)

    graph.add_node(
        node_id="addMemoryVariable1",
        module_type="addMemoryVariable",
        position={'x': 0, 'y': 1500},
        inputs=memory_variable_inputs
    )

    # 添加连接边
    graph.add_edge("simpleInputId", "pdf2md1", "finish", "switchAny")
    graph.add_edge("simpleInputId", "pdf2md1", "files", "files")
    graph.add_edge("simpleInputId", "addMemoryVariable1", "userChatInput", "question1_userChatInput")
    graph.add_edge("pdf2md1", "confirmreply1", "finish", "switchAny")
    graph.add_edge("pdf2md1", "addMemoryVariable1", "pdf2mdResult", "pdf2md1_pdf2mdResult")
    graph.add_edge("confirmreply1", "ai1", "finish", "switchAny")
    graph.add_edge("ai1", "addMemoryVariable1", "answerText", "ai1_answerText")

    # 编译,导入配置，点击确定
    graph.compile(
            name="从JSON生成的工作流",
            intro="这是从JSON数据反向生成的工作流",
            category="自动生成",
            prologue="你好！这是自动生成的工作流。",
            shareAble=True,
            allowVoiceInput=False,
            autoSendVoice=False
        )

if __name__ == "__main__":
    main()
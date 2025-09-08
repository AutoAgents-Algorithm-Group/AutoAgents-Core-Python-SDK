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
        }
    )

    graph.add_node(
        node_id="pdf2md1",
        module_type="pdf2md",
        position={'x': 500, 'y': 300},
        inputs={
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

    # 添加连接边
    graph.add_edge("simpleInputId", "pdf2md1", "finish", "switchAny")
    graph.add_edge("simpleInputId", "pdf2md1", "files", "files")
    graph.add_edge("pdf2md1", "confirmreply1", "finish", "switchAny")

    # 编译, 导入配置，点击确定
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
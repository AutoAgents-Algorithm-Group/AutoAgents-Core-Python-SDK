import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.autoagentsai.graph import FlowGraph, START
from src.autoagentsai.types import QuestionInputState, Pdf2MdState, ConfirmReplyState, AiChatState, AddMemoryVariableState


def main():
    """文档助手工作流 - 简洁的纯State API"""
    
    # 创建工作流图
    graph = FlowGraph(
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 设置起始节点
    graph.add_start_node(
        state=QuestionInputState(
            uploadFile=True
        )
    )

    # PDF转MD节点
    graph.add_node(
        id="pdf2md1",
        state=Pdf2MdState(
            pdf2mdType="deep_pdf2md"
        )
    )

    # 确认回复节点
    graph.add_node(
        id="confirmreply1",
        state=ConfirmReplyState(
            text=r"文件内容：{{@pdf2md1_pdf2mdResult}}",
            stream=True
        )
    )

    # AI对话节点
    graph.add_node(
        id="ai1",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""<角色>
你是一个文件解答助手，你可以根据文件内容，解答用户的问题
</角色>

<文件内容>
{{@pdf2md1_pdf2mdResult}}
</文件内容>

<用户问题>
{{@question1_userChatInput}}
</用户问题>
            """,
            knSearch="",
            temperature=0.1
        )
    )

    # 记忆变量节点
    graph.add_memory_variables(
        id="addMemoryVariable1",
        state=AddMemoryVariableState(
            variables={
                "question1_userChatInput": "string",
                "pdf2md1_pdf2mdResult": "string", 
                "ai1_answerText": "string"
            }
        )
    )

    # 连接节点
    graph.add_edge(START, "pdf2md1", "finish", "switchAny")
    graph.add_edge(START, "pdf2md1", "files", "files")
    graph.add_edge(START, "addMemoryVariable1", "userChatInput", "question1_userChatInput")
    graph.add_edge("pdf2md1", "confirmreply1", "finish", "switchAny")
    graph.add_edge("pdf2md1", "addMemoryVariable1", "pdf2mdResult", "pdf2md1_pdf2mdResult")
    graph.add_edge("confirmreply1", "ai1", "finish", "switchAny")
    graph.add_edge("ai1", "addMemoryVariable1", "answerText", "ai1_answerText")
    
    # 编译工作流
    graph.compile(
        name="文档助手",
        intro="这是一个专业的文档助手，可以帮助用户分析和理解文档内容",
        category="文档处理",
        prologue="你好！我是你的文档助手，请上传文档，我将帮您分析内容。"
    )


if __name__ == "__main__":
    main()
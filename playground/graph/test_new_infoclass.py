import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.autoagentsai.graph import FlowGraph
from src.autoagentsai.types import QuestionInputState, InfoClassState, ConfirmReplyState


def main():
    """测试信息分类工作流 - 简洁的纯State API"""
    
    # 创建工作流图
    graph = FlowGraph(
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )
    
    # 设置起始节点
    graph.add_start_node(
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            fileContrast=False,
            initialInput=True
        )
    )
    
    # 创建分类标签
    labels = {
        str(uuid.uuid1()): "买菜",
        str(uuid.uuid1()): "买肉"
    }

    # 创建信息分类节点
    graph.add_node(
        id="infoclass1",
        state=InfoClassState(
            model="doubao-deepseek-v3",
            quotePrompt="""请扮演文本分类器，根据信息输入和聊天上下文，判断输入信息属于哪种分类，以JSON格式输出分类信息。
            
            分类选项：
            - 买菜：用户想要购买蔬菜、水果等食材
            - 买肉：用户想要购买肉类产品
            
            请严格按照JSON格式返回结果。
            """,
            labels=labels,
            historyText=2
        )
    )
    
    # 创建回复节点 - 买菜
    graph.add_node(
        id="buyVeg",
        state=ConfirmReplyState(
            text="好的，我来帮您推荐一些新鲜的蔬菜和水果！请问您想要购买什么类型的蔬菜呢？",
            model="doubao-deepseek-v3"
        )
    )
    
    # 创建回复节点 - 买肉
    graph.add_node(
        id="buyMeat",
        state=ConfirmReplyState(
            text="好的，我来为您介绍一些优质肉类产品！请问您偏好哪种肉类呢？",
            model="doubao-deepseek-v3"
        )
    )
    
    # 连接节点
    graph.add_edge(graph.START, "infoclass1", "finish", "switchAny")
    graph.add_edge(graph.START, "infoclass1", "userChatInput", "text")
    graph.add_edge("infoclass1", "buyVeg", list(labels.keys())[0], "text")
    graph.add_edge("infoclass1", "buyMeat", list(labels.keys())[1], "text")
    
    # 编译工作流
    graph.compile(
        name="信息分类",
        intro="这是一个专业的信息分类系统",
        category="信息分类",
        prologue="你好！我是你的信息分类系统。"
    )


if __name__ == "__main__":
    main()
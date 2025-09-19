from ..client import ChatClient
from ..utils.extractor import extract_json
from typing import List, Optional


class SlideAgent:
    """
    PPT大纲生成代理
    
    主要功能：
    - 基于文档和提示生成PPT大纲
    - 通过AI智能分析内容结构
    
    注意：PPT填充功能请使用 PPTX2PPTXAgent 或 HTML2PPTXAgent
    """
    
    def __init__(self):
        pass

    def outline(self, prompt: str, file_path_list: Optional[List[str]] = None):
        """
        基于文档和提示生成PPT大纲
        
        Args:
            prompt: 生成大纲的提示文本
            file_path_list: 可选的参考文档文件路径列表
            
        Returns:
            str: 生成的PPT大纲文本
        """
        chat_client = ChatClient(
            agent_id="045c418f0dcf4adbb2f15031f06694d1",
            personal_auth_key="48cf18e0e0ca4b51bbf8fa60193ffb5c",
            personal_auth_secret="HWlQXZ5vxgrXDGEtTGGdsTFhJfr9rCmD",
            base_url="https://uat.agentspro.cn"
        )
    
        if file_path_list:
            print(f"Debug: 准备处理 {len(file_path_list)} 个文件: {file_path_list}")
        else:
            file_path_list = []
        
        content = ""
        try:
            for event in chat_client.invoke(prompt, files=file_path_list):
                if event['type'] == 'start_bubble':
                    print(f"\n{'=' * 20} 消息气泡{event['bubble_id']}开始 {'=' * 20}")
                elif event['type'] == 'token':
                    print(event['content'], end='', flush=True)
                    content += event['content']
                elif event['type'] == 'end_bubble':
                    print(f"\n{'=' * 20} 消息气泡结束 {'=' * 20}")
                elif event['type'] == 'finish':
                    print(f"\n{'=' * 20} 对话完成 {'=' * 20}")
                    break
                elif event['type'] == 'error':
                    print(f"\nDebug: 收到错误事件: {event}")
                    break
                    
        except Exception as e:
            print(f"\nDebug: ChatClient.invoke 发生异常: {type(e).__name__}: {e}")
            return f"生成大纲时发生错误: {str(e)}"
        
        # 尝试从返回内容中提取JSON结构化数据
        extracted_content = extract_json(content)
        if extracted_content:
            print(f"\nDebug: 成功提取JSON结构: {type(extracted_content)}")
            return extracted_content
        else:
            print(f"\nDebug: 未找到JSON结构，返回原始文本")
            return content
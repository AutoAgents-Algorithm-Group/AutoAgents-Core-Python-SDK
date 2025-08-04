import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


from autoagentsai import ChatClient, Publisher
    
def main():
    """原有的测试方法保持不变"""

    chat_client = ChatClient(
        agent_id="90b60436c09b43e5b6d05a31abf8c662",
        personal_auth_key="e7a964a7e754413a9ea4bc1395a38d39",
        personal_auth_secret="r4wBtqVD1qjItzQapJudKQPFozHAS9eb", 
    )
    
    publisher = Publisher(chat_client)

    result = publisher.publish_as_mcp(
        name="mcp-90b60436c09b43e5b6d05a31abf8c662",
        description="测试mcp",
        transport="streamable_http",
    )
    print("调用结果:", result)


if __name__ == "__main__":
    main()

import os
import sys

# 自动添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.client import ChatClient

client = ChatClient(
    agent_id="7e46d18945fc49379063e3057a143c58",
    personal_auth_key="339859fa69934ea8b2b0ebd19d94d7f1",
    personal_auth_secret="93TsBecJplOawEipqAdF7TJ0g4IoBMtA"
)

for event in client.invoke(prompt="人工智能的历史"):
    if event['type'] == 'start_bubble':
        print(f"\n{'=' * 20} 消息气泡{event['bubble_id']}开始 {'=' * 20}")
    elif event['type'] == 'reasoning_token':
        print(event['content'], end='', flush=True)
    elif event['type'] == 'token':
        print(event['content'], end='', flush=True)
    elif event['type'] == 'end_bubble':
        print(f"\n{'=' * 20} 消息气泡结束 {'=' * 20}")
    elif event['type'] == 'finish':
        print(f"\n{'=' * 20} 对话完成 {'=' * 20}")
        break

print(client.history())
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from src.autoagentsai.prebuilt import create_ppt_agent

def main():
    ppt_agent = create_ppt_agent()
    # ppt_agent.outline(prompt="请帮我生成一个PPT的大纲", file_path="论文润色版.pdf")
    # ppt_agent.cover()
    # ppt_agent.content()
    # ppt_agent.conclusion()
    # ppt_agent.save("论文润色版.pptx")
    ppt_agent.fill("自主规划智能体未来发展的pptx", "playground/ppt/template-1.pptx", "playground/ppt/output-1.pptx")

if __name__ == "__main__":
    main()
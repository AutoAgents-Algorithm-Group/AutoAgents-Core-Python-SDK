import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from src.autoagentsai.prebuilt import create_ppt_agent
from src.autoagentsai.prebuilt.create_html_agent import create_html_agent

def main():
    outline_agent = create_ppt_agent()  # 用于生成大纲的agent
    file_list = ["autoagents1.pdf", "产品介绍.pdf", "行业方案.pdf", "关于我们.pdf" ]
    outline_content = outline_agent.outline(
        prompt="请帮我基于这些文件生成一个综合的PPT大纲，整合所有文件的核心内容", 
        file_path=file_list
    )

    # 另一个agent用于生成PPT的html
    ppt_agent = create_html_agent()  # HELLOPPT
    
    ppt_agent.cover(outline_content=outline_content)
    ppt_agent.catalog(outline_content=outline_content)
    ppt_agent.content(outline_content=outline_content)
    ppt_agent.conclusion(outline_content=outline_content)
    
    print("所有HTML页面生成完成！")
    #ppt_agent.save("论文润色版.pptx")
    #ppt_agent.fill("自主规划智能体未来发展的pptx")

if __name__ == "__main__":
    main()
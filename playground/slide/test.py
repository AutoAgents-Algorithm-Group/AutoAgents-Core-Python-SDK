import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from src.autoagentsai.slide import create_ppt_agent

def main():
    ppt_agent = create_ppt_agent()
    template_path = "playground/test_workspace/test.pptx"
    output_path = "playground/test_workspace/fill_output.pptx"
    replacements = {
        "title": """# 项目概述
这是一个**重要的**项目演示。

* 第一个要点：*高效*的解决方案
* 第二个要点：`创新`的技术栈
* 第三个要点：**可靠**的`性能表现`

## 技术特性
- 支持**Markdown**格式
- 自动转换为PowerPoint格式
- 保持原有的*样式*和`结构`""",
        "logo": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png",
        "goods": [
            {
                "count": 4,
                "name": "**高级墙纸**",
                "desc": "* 书房专用\n* 卧室适配\n* `防水材质`",
                "discount": 1500,
                "tax": 27,
                "price": 400,
                "totalPrice": 1600,
                "picture": "globe.png"
            },
            {
                "count": 2,
                "name": "*经典地板*",
                "desc": "* 客厅铺设\n* **耐磨**材质\n* `环保认证`",
                "discount": 800,
                "tax": 15,
                "price": 600,
                "totalPrice": 1200,
                "picture": "floor.png"
            }
        ],
        "foods.name": [
            {
                "count": 222,
                "name": "**高级墙纸**",
                "desc": "* 书房专用\n* 卧室适配\n* `防水材质`",
                "discount": 1500,
                "tax": 27,
                "price": 400,
                "totalPrice": 1600,
                "picture": "globe.png"
            },
            {
                "count": 2,
                "name": "*经典地板*",
                "desc": "* 客厅铺设\n* **耐磨**材质\n* `环保认证`",
                "discount": 800,
                "tax": 15,
                "price": 600,
                "totalPrice": 1200,
                "picture": "floor.png"
            }
        ]
    }
    # ppt_agent.outline(prompt="请帮我生成一个PPT的大纲", file_path="论文润色版.pdf")
    # ppt_agent.cover()
    # ppt_agent.content()
    # ppt_agent.conclusion()
    # ppt_agent.save("论文润色版.pptx")
    ppt_agent.fill(replacements, template_path, output_path)

if __name__ == "__main__":
    main()
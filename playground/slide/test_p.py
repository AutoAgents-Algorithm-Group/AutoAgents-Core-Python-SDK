from autoagentsai.slide import create_ppt_agent

def main():
    ppt_agent = create_ppt_agent()
    template_path = "playground/test_workspace/test.pptx"
    output_path = "playground/test_workspace/fill_output.pptx"
    replacements = {
        "title": """# 你好sophia""",
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
            },
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
        "foods": [
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
    ppt_agent.fill(replacements, template_path, output_path)

if __name__ == "__main__":
    main()
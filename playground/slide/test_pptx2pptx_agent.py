import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.autoagents_core.slide import PPTX2PPTXAgent

def main():
    
    agent = PPTX2PPTXAgent() 

    # 1. 原始数据
    source_data = {
        "cover": {
            "title": "年度总结报告", 
            "subtitle": "战略发展部",
            "author": "张经理",
            "date": "2024年12月"
        },
        "achievements": [
            {
                "title": "重要成就",
                "subtitle": "融资成功",
                "desc": "完成了A轮融资，金额超预期。",
                "details": "• 获得知名投资机构青睐\n• 融资金额达5000万元\n• 将用于产品研发和市场拓展"
            },
            {
                "title": "重要成就", 
                "subtitle": "用户突破",
                "desc": "核心产品用户数突破100万大关。",
                "details": "• 月活跃用户增长300%\n• 用户满意度高达95%\n• 市场占有率稳步提升"
            }
        ],
        "challenges": [
            {
                "title": "面临挑战",
                "subtitle": "市场竞争",
                "desc": "市场竞争加剧，需要寻找新的突破口。",
                "solutions": "• 加强产品创新\n• 提升用户体验\n• 拓展新的市场领域"
            },
        ],
        "future": {
            "title": "未来计划",
            "focus": "重点投入AI驱动的新产品线研发。",
            "key_initiatives": "• 组建AI研发团队\n• 建立技术创新中心\n• 推出智能化产品\n• 拓展企业级市场",
            "investments": "总投资计划1.2亿元"
        }
    }

    # 2. 定义渲染指令
    order_info = [
        (0, "cover"),      # 模板0, 封面
        (1, "achievements[0]"),   # 模板1, 成就页
        (1, "achievements[1]"),   # 模板1, 成就页
        (1, "achievements[1]"),   # 模板1, 成就页
        (1, "achievements[1]"),   # 模板1, 成就页
        (1, "achievements[1]"),   # 模板1, 成就页
        (2, "challenges[0]"),     # 模板2, 挑战页
        (3, "future"),    # 模板3, 计划页
    ]

    try:
        # 3. 调用
        # order_info 参数直接传递指令列表
        result = agent.fill(
            data=source_data,
            template_file_path="playground/slide/input/test_template_with_order_info.pptx",
            output_file_path="playground/slide/output/test_pptx2pptx_with_order_info.pptx",
            order_info=order_info,
            verbose=True
        )
        # 不使用order_info
        result = agent.fill(
            data=source_data,
            template_file_path="playground/slide/input/test.pptx",
            output_file_path="playground/slide/output/test_pptx2pptx_wo_order_info.pptx",
            # order_info=order_info,
            verbose=True
        )
        
        print(f"📁 输出文件: {result}")
        
    except Exception as e:
        print(f"❌ 调用失败: {e}")

if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("playground/slide/output", exist_ok=True)
    main()
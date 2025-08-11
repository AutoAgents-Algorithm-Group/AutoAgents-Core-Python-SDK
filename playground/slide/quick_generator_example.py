"""
动态PPT内容生成器快速使用示例
============================

这个示例展示了如何快速使用DynamicSlideAgent生成PPT内容，
生成的内容可以直接用于SlideAgent进行PPT填充。
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.slide import DynamicSlideAgent, SlideAgent


def quick_generate_example():
    """快速生成PPT内容的简单示例"""
    
    # 1. 创建动态生成器
    generator = DynamicSlideAgent()
    
    # 2. 定义PPT需求
    ppt_request = """
    创建一个关于"人工智能在企业中的应用"的商业演示PPT，包括：
    - 封面页（包含主标题和公司Logo）
    - AI技术概述
    - 在不同行业的应用案例（包含数据表格）
    - 实施方案和步骤
    - ROI分析和效益预测
    - 联系方式页面
    生成6页专业内容。
    """
    
    # 3. 生成PPT内容
    print("🚀 开始生成PPT内容...")
    
    result = generator.generate_slide_content(
        user_request=ppt_request,
        pages_count=6,
        include_images=True,
        include_tables=True
    )
    
    # 4. 验证和保存结果
    if generator.validate_slide_structure(result):
        print("✅ PPT内容生成成功！")
        
        # 保存为JSON文件
        output_file = "playground/slide/ai_business_ppt.json"
        generator.export_to_json_file(result, output_file)
        
        # 显示生成的页面信息
        pages = result.get('page', [])
        print(f"\n📄 生成了 {len(pages)} 页内容：")
        for i, page in enumerate(pages):
            title = page.get('title', f'第{i+1}页')
            print(f"  {i+1}. {title}")
            
            # 显示每页包含的内容类型
            content_types = []
            if 'subtitle' in page:
                content_types.append("副标题")
            if 'logo' in page or any(key.startswith('@') for key in str(page)):
                content_types.append("图片")
            if 'sections' in page:
                content_types.append(f"{len(page['sections'])}个章节")
            if 'table' in page:
                content_types.append("数据表格")
            if 'content' in page:
                content_types.append("主要内容")
                
            if content_types:
                print(f"     包含: {', '.join(content_types)}")
        
        print(f"\n💾 内容已保存到: {output_file}")
        print("\n🎯 下一步：可以使用SlideAgent.fill()方法将此内容填充到PPT模板中")
        
        return result
        
    else:
        print("❌ 生成的内容结构验证失败")
        return None


def template_based_example():
    """基于模板的快速生成示例"""
    
    generator = DynamicSlideAgent()
    
    print("\n🎨 使用模板快速生成...")
    
    # 自定义数据
    project_data = {
        "项目名称": "智慧城市数据平台",
        "客户": "某市政府",
        "项目周期": "12个月", 
        "团队规模": "25人",
        "预算": "500万元",
        "核心技术": "大数据分析、IoT、AI预测",
        "预期收益": "提升城市管理效率30%"
    }
    
    # 使用商业模板生成
    result = generator.generate_with_template(
        template_type="business",
        custom_data=project_data,
        pages_count=5
    )
    
    if generator.validate_slide_structure(result):
        print("✅ 模板生成成功！")
        
        output_file = "playground/slide/smart_city_ppt.json"
        generator.export_to_json_file(result, output_file)
        
        pages = result.get('page', [])
        print(f"📄 基于business模板生成了 {len(pages)} 页内容")
        
        return result
    else:
        print("❌ 模板生成失败")
        return None


def show_placeholder_examples():
    """展示占位符的实际应用示例"""
    
    print("\n" + "="*50)
    print("📋 占位符使用指南")
    print("="*50)
    
    examples = [
        {
            "类型": "文本占位符",
            "格式": "{{path}}",
            "示例": "{{page[0].title}}",
            "说明": "获取第1页的标题文本"
        },
        {
            "类型": "图片占位符", 
            "格式": "{{@path}}",
            "示例": "{{@page[0].logo}}",
            "说明": "显示第1页的logo图片"
        },
        {
            "类型": "表格占位符",
            "格式": "{{#path}}", 
            "示例": "{{#page[1].table}}",
            "说明": "填充第2页的表格数据"
        },
        {
            "类型": "章节内容",
            "格式": "{{path}}",
            "示例": "{{page[1].sections[0].content}}",
            "说明": "获取第2页第1个章节的内容"
        }
    ]
    
    for example in examples:
        print(f"\n🔹 {example['类型']}")
        print(f"   格式: {example['格式']}")
        print(f"   示例: {example['示例']}")
        print(f"   说明: {example['说明']}")
    
    print(f"\n💡 实际使用流程：")
    print("1. 使用DynamicSlideAgent生成JSON格式的PPT内容")
    print("2. 在PPT模板中放置对应的占位符文本框")
    print("3. 使用SlideAgent.fill()方法自动填充内容")
    print("4. 生成最终的PPT文件")


if __name__ == "__main__":
    print("🎯 动态PPT内容生成器 - 快速使用示例")
    print("="*50)
    
    # 基础生成示例
    result1 = quick_generate_example()
    
    # 模板生成示例
    result2 = template_based_example()
    
    # 显示占位符使用指南
    show_placeholder_examples()
    
    print(f"\n🎉 示例运行完成！")
    print("📁 查看playground/slide/目录下生成的JSON文件")
    print("📖 参考test_dynamic_generator.py获取更多高级用法")
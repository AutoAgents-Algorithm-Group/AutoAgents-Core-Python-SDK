import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.slide import DynamicSlideAgent


def main():
    """演示动态PPT内容生成器的各种使用方式"""
    
    # 创建动态PPT生成器
    dynamic_agent = DynamicSlideAgent()
    
    print("=" * 60)
    print("动态PPT内容生成器测试")
    print("=" * 60)
    
    # 测试1: 基础内容生成
    print("\n🚀 测试1: 基础内容生成")
    print("-" * 40)
    
    business_request = """
    请为我们公司创建一个产品发布会的PPT，产品名称是"智能排班系统"。
    内容应该包括：
    1. 产品介绍页面
    2. 核心功能展示  
    3. 技术架构说明
    4. 市场优势分析
    5. 客户案例展示
    6. 价格方案
    请生成6页内容，包含图表和数据展示。
    """
    
    try:
        result1 = dynamic_agent.generate_slide_content(
            user_request=business_request,
            pages_count=6,
            include_images=True,
            include_tables=True
        )
        
        if dynamic_agent.validate_slide_structure(result1):
            print("✅ 生成成功！")
            print(f"📄 生成了 {len(result1.get('page', []))} 页内容")
            
            # 保存结果
            output_file1 = "playground/slide/generated_business_ppt.json"
            dynamic_agent.export_to_json_file(result1, output_file1)
            
            # 显示前两页的结构
            print("\n📋 前两页内容预览：")
            for i, page in enumerate(result1.get('page', [])[:2]):
                print(f"第{page.get('page_number', i+1)}页: {page.get('title', '无标题')}")
                if 'sections' in page:
                    for section in page['sections'][:2]:  # 只显示前2个章节
                        print(f"  - {section.get('title', '无标题')}")
        else:
            print("❌ 生成的结构验证失败")
            
    except Exception as e:
        print(f"❌ 生成失败: {e}")
    
    
    # 测试2: 使用模板生成
    print("\n🎯 测试2: 使用技术模板生成")
    print("-" * 40)
    
    custom_data = {
        "技术栈": "Python, React, PostgreSQL",
        "项目名称": "AI自动化工作流平台", 
        "团队规模": "8人",
        "开发周期": "6个月",
        "目标用户": "企业客户和开发者"
    }
    
    try:
        result2 = dynamic_agent.generate_with_template(
            template_type="technology",
            custom_data=custom_data,
            pages_count=5
        )
        
        if dynamic_agent.validate_slide_structure(result2):
            print("✅ 模板生成成功！")
            print(f"📄 生成了 {len(result2.get('page', []))} 页内容")
            
            # 保存结果
            output_file2 = "playground/slide/generated_tech_ppt.json"
            dynamic_agent.export_to_json_file(result2, output_file2)
            
        else:
            print("❌ 模板生成的结构验证失败")
            
    except Exception as e:
        print(f"❌ 模板生成失败: {e}")
    
    
    # 测试3: 教育培训内容生成
    print("\n📚 测试3: 教育培训内容生成")
    print("-" * 40)
    
    education_request = """
    创建一个关于"Python编程基础"的培训课程PPT，包括：
    - 课程介绍和目标
    - Python语法基础
    - 数据类型和变量
    - 控制流程（条件和循环）
    - 函数定义和使用
    - 实战案例
    - 课后练习
    请生成7页内容，包含代码示例和练习题。
    """
    
    try:
        result3 = dynamic_agent.generate_slide_content(
            user_request=education_request,
            pages_count=7,
            include_images=False,  # 教育内容主要是文本
            include_tables=True
        )
        
        if dynamic_agent.validate_slide_structure(result3):
            print("✅ 教育内容生成成功！")
            print(f"📄 生成了 {len(result3.get('page', []))} 页内容")
            
            # 保存结果
            output_file3 = "playground/slide/generated_education_ppt.json"
            dynamic_agent.export_to_json_file(result3, output_file3)
            
        else:
            print("❌ 教育内容结构验证失败")
            
    except Exception as e:
        print(f"❌ 教育内容生成失败: {e}")


    # 测试4: 数据分析报告
    print("\n📊 测试4: 数据分析报告生成")
    print("-" * 40)
    
    report_request = """
    创建一个季度销售数据分析报告PPT，包括：
    - 报告概要
    - 销售数据总览（包含具体数字表格）
    - 各产品线表现对比
    - 区域销售分析
    - 客户满意度调查结果
    - 问题分析和改进建议
    - 下季度目标制定
    请生成包含丰富数据表格的8页内容。
    """
    
    try:
        result4 = dynamic_agent.generate_slide_content(
            user_request=report_request,
            pages_count=8,
            include_images=True,
            include_tables=True
        )
        
        if dynamic_agent.validate_slide_structure(result4):
            print("✅ 数据报告生成成功！")
            print(f"📄 生成了 {len(result4.get('page', []))} 页内容")
            
            # 保存结果  
            output_file4 = "playground/slide/generated_report_ppt.json"
            dynamic_agent.export_to_json_file(result4, output_file4)
            
            # 检查表格数据
            table_pages = [p for p in result4.get('page', []) if 'table' in p]
            print(f"📈 包含表格的页面数: {len(table_pages)}")
            
        else:
            print("❌ 数据报告结构验证失败")
            
    except Exception as e:
        print(f"❌ 数据报告生成失败: {e}")


    print("\n" + "=" * 60)
    print("✨ 动态PPT内容生成器测试完成")
    print("=" * 60)
    
    print("\n💡 使用提示：")
    print("1. 生成的JSON文件可以直接用于SlideAgent.fill()方法")
    print("2. 支持的占位符格式：")
    print("   - {{path}} : 文本内容")
    print("   - {{@path}} : 图片占位符") 
    print("   - {{#path}} : 表格占位符")
    print("3. 生成的内容支持Markdown格式（粗体、斜体、代码等）")
    print("4. 表格数据可以是CSV文件路径或JSON数组")
    print("5. 可以通过template_type使用预设模板快速生成特定类型内容")


def demo_placeholder_usage():
    """演示占位符的实际使用方法"""
    
    print("\n🔧 占位符使用演示")
    print("-" * 40)
    
    # 创建示例数据（类似test_data格式）
    sample_data = {
        "company": {
            "name": "智能科技有限公司",
            "logo": "company_logo.png",
            "slogan": "创新驱动未来"
        },
        "product": {
            "name": "智能排班系统",
            "version": "v2.0",
            "features": ["AI算法优化", "实时数据同步", "移动端支持"]
        },
        "sales_data": [
            {"month": "1月", "revenue": 150000, "growth": "15%"},
            {"month": "2月", "revenue": 180000, "growth": "20%"},
            {"month": "3月", "revenue": 220000, "growth": "22%"}
        ]
    }
    
    print("📋 示例数据结构：")
    print(json.dumps(sample_data, ensure_ascii=False, indent=2))
    
    print("\n🎯 对应的占位符使用：")
    placeholders = [
        "{{company.name}} - 获取公司名称",
        "{{@company.logo}} - 显示公司Logo图片", 
        "{{product.name}} - 获取产品名称",
        "{{product.features}} - 显示功能列表（自动转为bullet points）",
        "{{#sales_data}} - 显示销售数据表格"
    ]
    
    for placeholder in placeholders:
        print(f"  • {placeholder}")
    
    print("\n⚡ 在PPT模板中的实际应用：")
    print("  • 标题文本框：{{company.name}}")
    print("  • 图片占位符：{{@company.logo}}")  
    print("  • 表格占位符：{{#sales_data}}")
    print("  • 列表内容：{{product.features}}")


if __name__ == "__main__":
    main()
    demo_placeholder_usage()
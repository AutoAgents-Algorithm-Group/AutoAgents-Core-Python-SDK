#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPTX2PPTXAgent测试文件
测试PPTX模板填充和动态重排序功能
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.autoagentsai.slide.pptx2pptx_agent import PPTX2PPTXAgent

def create_test_data():
    """创建测试数据"""
    return {
        "presentation": {
            "title": "智能科技解决方案",
            "subtitle": "引领未来的创新技术",
            "date": "2024年12月"
        },
        "presenter": {
            "name": "张技术",
            "contact": "zhang@tech.com"
        },
        "company": {
            "name": "创新科技有限公司",
            "description": "我们专注于人工智能和机器学习解决方案的研发",
            "founded": "2020年",
            "employees": "150",
            "customers": "500+",
            "revenue": "5000万元",
            "logo": "https://via.placeholder.com/200x100/0066CC/FFFFFF?text=LOGO",
            "team_photo": "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=TEAM"
        },
        "products": [
            {
                "name": "智能助手 Pro 3.0",
                "price": "¥299/月",
                "features": ["自然语言理解", "多模态交互", "智能任务规划", "企业级安全"],
                "detailed_features": [
                    "• 支持文字、语音、图片多种输入方式",
                    "• 智能理解上下文，提供精准回答", 
                    "• 自动任务规划和执行",
                    "• 企业级数据安全保护",
                    "• 24/7全天候服务支持"
                ],
                "image": "https://via.placeholder.com/400x300/FF9800/FFFFFF?text=PRODUCT"
            }
        ],
        "financial_data": [
            {"项目": "营收", "Q1": "1000万", "Q2": "1200万", "Q3": "1500万"},
            {"项目": "利润", "Q1": "200万", "Q2": "300万", "Q3": "450万"},
            {"项目": "用户数", "Q1": "5万", "Q2": "8万", "Q3": "12万"}
        ],
        "charts": {
            "revenue_trend": "https://via.placeholder.com/600x400/2196F3/FFFFFF?text=REVENUE+CHART"
        },
        "achievements": [
            "成功发布智能助手3.0版本",
            "用户数量突破10万大关", 
            "获得行业最佳创新奖",
            "完成B轮融资3000万",
            "建立5个城市服务中心"
        ],
        "next_steps": [
            "Q3推出移动端应用",
            "扩展企业级功能模块",
            "建设开发者生态",
            "进军国际市场", 
            "启动IPO准备工作"
        ]
    }

def test_basic_fill():
    """测试基本填充功能（使用原始顺序）"""
    print("🧪 测试1: 基本填充功能")
    print("-" * 40)
    
    agent = PPTX2PPTXAgent()
    data = create_test_data()
    
    try:
        result = agent.fill(
            data=data,
            template_file_path="playground/slide/input/test_template.pptx",
            output_file_path="playground/slide/output/basic_fill_result.pptx",
            verbose=True
        )
        print(f"✅ 基本填充成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 基本填充失败: {e}")
        return False

def test_reorder_fill():
    """测试重排序填充功能"""
    print("\n🧪 测试2: 重排序填充功能") 
    print("-" * 40)
    
    agent = PPTX2PPTXAgent()
    data = create_test_data()
    
    # 投资人路演场景：突出数据和成果
    order_info = {
        "order": [0, 1, 3, 3, 3, 3, 3, 4],  # 封面 -> 公司介绍 -> 数据 -> 再次数据 -> 总结
        "mapping": {
            "cover": [0],
            "company": [1], 
            "product": [2],
            "data": [3],
            "summary": [4]
        }
    }
    
    try:
        result = agent.fill(
            data=data,
            template_file_path="playground/slide/input/test_template.pptx",
            output_file_path="playground/slide/output/reorder_fill_result.pptx",
            order_info=order_info,
            verbose=True
        )
        print(f"✅ 重排序填充成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 重排序填充失败: {e}")
        return False

def test_base64_output():
    """测试Base64输出格式"""
    print("\n🧪 测试3: Base64输出格式")
    print("-" * 40)
    
    agent = PPTX2PPTXAgent()
    data = create_test_data()
    
    try:
        result = agent.fill(
            data=data,
            template_file_path="playground/slide/input/test_template.pptx",
            output_format="base64",
            verbose=False
        )
        
        # 保存base64到文件
        with open("output/base64_result.txt", "w") as f:
            f.write(result)
            
        print(f"✅ Base64输出成功，长度: {len(result)} 字符")
        print(f"📁 Base64内容已保存到: output/base64_result.txt")
        return True
    except Exception as e:
        print(f"❌ Base64输出失败: {e}")
        return False

def test_multiple_data_fill():
    """测试多数据填充功能 - 同一模板页面填入不同内容"""
    print("\n🧪 测试4: 多数据填充功能")
    print("-" * 40)
    
    agent = PPTX2PPTXAgent()
    
    # 创建多个员工的数据
    employees_data = [
        {
            "presentation": {"title": "员工档案", "date": "2024年12月"},
            "presenter": {"name": "张技术", "contact": "zhang@tech.com"},
            "company": {
                "name": "创新科技有限公司",
                "description": "优秀员工：张三",
                "founded": "2020年",
                "employees": "150",
                "logo": "https://via.placeholder.com/200x100/0066CC/FFFFFF?text=LOGO"
            },
            "products": [{
                "name": "个人表现评估",
                "price": "优秀",
                "features": ["技术能力强", "团队合作好", "创新思维", "责任心强"]
            }]
        },
        {
            "presentation": {"title": "员工档案", "date": "2024年12月"},
            "presenter": {"name": "李技术", "contact": "li@tech.com"},
            "company": {
                "name": "创新科技有限公司", 
                "description": "优秀员工：李四",
                "founded": "2020年",
                "employees": "150",
                "logo": "https://via.placeholder.com/200x100/4CAF50/FFFFFF?text=LOGO"
            },
            "products": [{
                "name": "个人表现评估",
                "price": "良好",
                "features": ["学习能力强", "沟通能力好", "执行力强", "积极主动"]
            }]
        },
        {
            "presentation": {"title": "员工档案", "date": "2024年12月"},
            "presenter": {"name": "王技术", "contact": "wang@tech.com"},
            "company": {
                "name": "创新科技有限公司",
                "description": "优秀员工：王五",
                "founded": "2020年", 
                "employees": "150",
                "logo": "https://via.placeholder.com/200x100/FF9800/FFFFFF?text=LOGO"
            },
            "products": [{
                "name": "个人表现评估",
                "price": "优秀",
                "features": ["领导能力强", "解决问题能力", "创新能力", "团队建设"]
            }]
        }
    ]
    
    try:
        result = agent.fill_multiple_data(
            data_list=employees_data,
            template_file_path="playground/slide/input/test_template.pptx",
            template_slide_index=0,  # 使用第一页作为模板
            output_file_path="playground/slide/output/multiple_employees.pptx",
            verbose=True
        )
        print(f"✅ 多数据填充成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 多数据填充失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 PPTX2PPTXAgent 功能测试")
    print("=" * 50)
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 运行测试
    results = []
    results.append(test_basic_fill())
    results.append(test_reorder_fill()) 
    results.append(test_base64_output())
    results.append(test_multiple_data_fill())
    
    # 测试结果总结
    print("\n📊 测试结果总结")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    test_names = ["基本填充", "重排序填充", "Base64输出", "多数据填充"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n🎯 总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    print("\n📁 输出文件:")
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith(('.pptx', '.txt')):
                print(f"  • output/{file}")

if __name__ == "__main__":
    main()
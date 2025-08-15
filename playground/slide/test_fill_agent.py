#!/usr/bin/env python3
"""
测试嵌套JSON结构的PPT填充
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.autoagentsai.slide.FillAgent import FillAgent

def main():
    """主测试函数"""
    print("🧪 测试嵌套JSON结构PPT填充")
    print("=" * 50)

    # 测试数据 - 嵌套JSON结构
    data = {
        "user": {
            "nickname": "frank",
            "age": 21,
            "department": "技术部",
            "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
            "hobbies": ["编程", "阅读", "游泳", "摄影"],
            "skills": ["Python", "JavaScript", "React", "机器学习"],
            "contact": {
                "email": "frank@company.com",
                "phone": "13800138000"
            },
            "dad": {
                "nickname": "frank-dad",
                "age": 45,
                "job": {
                    "title": "高级工程师",
                    "company": "科技集团"
                }
            }
        },
        "company": {
            "name": "创新科技公司",
            "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=300&h=200&fit=crop"
        },
        "family": {
            "photo": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=400&h=300&fit=crop",
            "members": [
                {"name": "frank", "role": "儿子", "age": 21},
                {"name": "frank-dad", "role": "父亲", "age": 45},
                {"name": "mom", "role": "母亲", "age": 42}
            ]
        },
        "work": {
            "current_project": {
                "name": "AI助手系统",
                "manager": "张经理",
                "progress": 75,
                "deadline": "2024-06-30"
            },
            "projects": [
                {"name": "项目A", "status": "已完成", "progress": 100},
                {"name": "项目B", "status": "进行中", "progress": 60},
                {"name": "项目C", "status": "计划中", "progress": 0}
            ]
        },
        "evaluation": {
            "score": 95,
            "comment": "表现优秀，技术能力强，团队合作佳"
        }
    }
    
    # 创建FillAgent
    fill_agent = FillAgent()
    
    # 模板和输出路径
    template_path = "playground/test_workspace/template/test_template.pptx"
    output_path = "playground/test_workspace/output/test_output.pptx"
    
    try:
        print(f"\n🔍 开始填充PPT...")
        print(f"模板: {template_path}")
        print(f"输出: {output_path}")
        
        result = fill_agent.fill(
            data=data,
            template_file_path=template_path,
            output_file_path=output_path,
            output_format="local"
        )
        
        print(f"\n✅ PPT填充成功!")
        print(f"📄 输出文件: {result}")
        print(f"\n💡 请打开 {output_path} 查看结果")
        
    except Exception as e:
        print(f"❌ 填充失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

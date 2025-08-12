#!/usr/bin/env python3
"""
FillAgent 独立填充代理使用示例
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.autoagentsai.slide.FillAgent import FillAgent


def test_local_output():
    """测试本地文件输出格式"""
    
    # 创建填充代理
    fill_agent = FillAgent()
    
    # 示例数据
    data = {
        "page": [
            { 
                "page_number": 1,
                "title": "智能排班系统",
                "subtitle": "提升工作效率的解决方案",
                "logo": "company_logo.png"
            },
            { 
                "page_number": 2,
                "title": "核心需求",
                "sections": [
                    { "title": "精准计算", "content": "基于AI算法的精确计算，确保排班公平性和效率" },
                    { "title": "自动排班", "content": "智能化排班系统，减少人工干预，提高管理效率" }
                ]
            },
            {
                "page_number": 3,
                "title": "系统架构",
                "table": "playground/test_workspace/data.csv"
            },
            {
                "page_number": 4,
                "title": "商品列表",
                "table": [
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
                ]
            }
        ]
    }
    
    template_path = "playground/test_workspace/template/test.pptx"
    output_path = "playground/test_workspace/output_local.pptx"
    
    try:
        result = fill_agent.fill(data, template_path, output_path, output_format="local")
        print(f"✅ 本地文件输出完成: {result}")
    except Exception as e:
        print(f"❌ 本地文件输出失败: {e}")


def test_base64_output():
    """测试base64输出格式"""
    
    # 创建填充代理
    fill_agent = FillAgent()
    
    # 简化的测试数据
    data = {
        "page": [
            { 
                "page_number": 1,
                "title": "智能排班系统",
                "subtitle": "提升工作效率的解决方案",
                "logo": "company_logo.png"
            },
            { 
                "page_number": 2,
                "title": "核心需求",
                "sections": [
                    { "title": "精准计算", "content": "基于AI算法的精确计算，确保排班公平性和效率" },
                    { "title": "自动排班", "content": "智能化排班系统，减少人工干预，提高管理效率" }
                ]
            },
            {
                "page_number": 3,
                "title": "系统架构",
                "table": "playground/test_workspace/data.csv"
            },
            {
                "page_number": 4,
                "title": "商品列表",
                "table": [
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
                ]
            }
        ]
    }
    
    template_path = "https://pefile.oss-cn-beijing.aliyuncs.com/frank/test.pptx"
    
    try:
        result = fill_agent.fill(data, template_path, output_format="base64")
        print(f"✅ Base64输出完成 (长度: {len(result)} 字符)")
        print(f"Base64前缀: {result}...")
    except Exception as e:
        print(f"❌ Base64输出失败: {e}")


def test_url_output():
    """测试URL上传输出格式"""
    
    # 创建填充代理
    fill_agent = FillAgent()
    
    # 简化的测试数据
    data = {
        "page": [
            { 
                "page_number": 1,
                "title": "智能排班系统",
                "subtitle": "提升工作效率的解决方案",
                "logo": "company_logo.png"
            },
            { 
                "page_number": 2,
                "title": "核心需求",
                "sections": [
                    { "title": "精准计算", "content": "基于AI算法的精确计算，确保排班公平性和效率" },
                    { "title": "自动排班", "content": "智能化排班系统，减少人工干预，提高管理效率" }
                ]
            },
            {
                "page_number": 3,
                "title": "系统架构",
                "table": "playground/test_workspace/data.csv"
            },
            {
                "page_number": 4,
                "title": "商品列表",
                "table": [
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
                ]
            }
        ]
    }
    
    template_path = "https://pefile.oss-cn-beijing.aliyuncs.com/frank/test.pptx"
    
    # 这里需要真实的JWT token，示例中使用占位符
    personal_auth_key = "7217394b7d3e4becab017447adeac239"  # 请替换为真实的JWT token
    personal_auth_secret = "f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB"  # 请替换为真实的JWT token
    
    try:
        result = fill_agent.fill(
            data, 
            template_path, 
            output_format="url",
            personal_auth_key=personal_auth_key,
            personal_auth_secret=personal_auth_secret
        )
        print(f"✅ URL上传完成:")
        print(f"  文件ID: {result.get('fileId')}")
        print(f"  文件名: {result.get('fileName')}")
        print(f"  文件类型: {result.get('fileType')}")
    except Exception as e:
        print(f"❌ URL上传失败: {e}")
        if "jwt_token" in str(e):
            print("  注意: 需要提供有效的JWT token才能测试URL上传功能")


if __name__ == "__main__":
    print("=== FillAgent 多种输出格式测试 ===\n")
    
    print("1. 测试本地文件输出...")
    test_local_output()
    print()
    
    print("2. 测试Base64输出...")
    test_base64_output()
    print()
    
    print("3. 测试URL上传输出...")
    test_url_output()
    print()
 
    print("=== 测试完成 ===")
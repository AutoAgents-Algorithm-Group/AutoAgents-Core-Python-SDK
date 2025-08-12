import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.slide import SlideAgent


def get_test_data():
    """获取测试数据"""
    return {
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


def test_local_output():
    """测试本地文件输出格式"""
    
    print("1. 测试本地文件输出...")
    
    slide_agent = SlideAgent()
    test_data = get_test_data()
    
    template_path = "playground/test_workspace/template/test.pptx"
    output_path = "playground/test_workspace/slide_agent_local.pptx"
    
    try:
        result = slide_agent.fill(test_data, template_path, output_path, output_format="local")
        print(f"✅ 本地文件输出完成: {result}")
    except Exception as e:
        print(f"❌ 本地文件输出失败: {e}")


def test_base64_output():
    """测试base64输出格式"""
    
    print("2. 测试Base64输出...")
    
    slide_agent = SlideAgent()
    test_data = get_test_data()
    
    template_path = "https://pefile.oss-cn-beijing.aliyuncs.com/frank/test.pptx"
    
    try:
        result = slide_agent.fill(test_data, template_path, output_format="base64")
        print(f"✅ Base64输出完成 (长度: {len(result)} 字符)")
        print(f"Base64前缀: {result[:50]}...")
    except Exception as e:
        print(f"❌ Base64输出失败: {e}")


def test_url_output():
    """测试URL上传输出格式"""
    
    print("3. 测试URL上传输出...")
    
    slide_agent = SlideAgent()
    test_data = get_test_data()
    
    template_path = "https://pefile.oss-cn-beijing.aliyuncs.com/frank/test.pptx"
    
    # 这里需要真实的认证密钥
    personal_auth_key = "7217394b7d3e4becab017447adeac239"
    personal_auth_secret = "f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB"
    
    try:
        result = slide_agent.fill(
            test_data, 
            template_path, 
            output_format="url",
            personal_auth_key=personal_auth_key,
            personal_auth_secret=personal_auth_secret
        )
        print(f"✅ URL上传完成:")
        print(f"  文件ID: {result.get('fileId')}")
        print(f"  文件URL: {result.get('fileUrl')}")
    except Exception as e:
        print(f"❌ URL上传失败: {e}")
        if "personal_auth_key" in str(e):
            print("  注意: 需要提供有效的认证密钥才能测试URL上传功能")


def main():
    """主测试函数"""
    print("=== SlideAgent 多种输出格式测试 ===\n")
    
    test_local_output()
    print()
    
    test_base64_output()
    print()
    
    test_url_output()
    print()
    
    print("=== 测试完成 ===")


if __name__ == "__main__":
    main() 
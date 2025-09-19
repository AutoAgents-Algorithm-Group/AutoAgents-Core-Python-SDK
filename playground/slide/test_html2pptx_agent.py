#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML2PPTXAgent测试文件
测试HTML到PPTX转换功能
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.autoagents_core.slide import HTML2PPTXAgent

def create_test_html_content():
    """创建测试用的HTML内容"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试演示文稿</title>
        <style>
            .slide {
                padding: 20px;
                margin: 20px 0;
                border: 2px solid #0066CC;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
            }
            .slide h1 {
                font-size: 28px;
                color: #FFD700;
                text-align: center;
                margin-bottom: 20px;
            }
            .slide h2 {
                font-size: 24px;
                color: #FFF;
                margin-bottom: 15px;
            }
            .slide p {
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 10px;
            }
            .slide ul {
                margin-left: 20px;
            }
            .slide li {
                margin-bottom: 8px;
            }
            .highlight {
                background-color: #FF6B6B;
                padding: 2px 6px;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <!-- 第一页：封面 -->
        <div class="slide">
            <h1>🚀 创新科技解决方案</h1>
            <p style="text-align: center; font-size: 20px;">引领未来的智能化发展</p>
            <p style="text-align: center; font-size: 16px;">演讲人：张技术总监</p>
            <p style="text-align: center; font-size: 16px;">2024年12月</p>
        </div>

        <!-- 第二页：公司介绍 -->
        <div class="slide">
            <h1>💼 关于我们</h1>
            <h2>创新科技有限公司</h2>
            <p>我们是一家专注于<span class="highlight">人工智能</span>和<span class="highlight">机器学习</span>解决方案的创新企业。</p>
            
            <h2>核心数据</h2>
            <ul>
                <li>🏢 成立时间：2020年</li>
                <li>👥 员工数量：150人</li>
                <li>🤝 服务客户：500+</li>
                <li>💰 年营收：5000万元</li>
            </ul>
        </div>

        <!-- 第三页：产品展示 -->
        <div class="slide">
            <h1>🎯 核心产品</h1>
            <h2>智能助手 Pro 3.0</h2>
            <p><strong>价格：</strong>¥299/月</p>
            
            <h2>核心特性</h2>
            <ul>
                <li>🧠 自然语言理解</li>
                <li>🎨 多模态交互</li>
                <li>📋 智能任务规划</li>
                <li>🔒 企业级安全</li>
            </ul>
            
            <h2>详细功能</h2>
            <ul>
                <li>支持文字、语音、图片多种输入方式</li>
                <li>智能理解上下文，提供精准回答</li>
                <li>自动任务规划和执行</li>
                <li>企业级数据安全保护</li>
                <li>24/7全天候服务支持</li>
            </ul>
        </div>

        <!-- 第四页：数据展示 -->
        <div class="slide">
            <h1>📊 业务数据</h1>
            <h2>季度财务表现</h2>
            
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3>营收增长</h3>
                <p>Q1: 1000万 → Q2: 1200万 → Q3: 1500万</p>
                
                <h3>利润提升</h3>
                <p>Q1: 200万 → Q2: 300万 → Q3: 450万</p>
                
                <h3>用户增长</h3>
                <p>Q1: 5万 → Q2: 8万 → Q3: 12万</p>
            </div>
        </div>

        <!-- 第五页：总结 -->
        <div class="slide">
            <h1>🎉 总结与展望</h1>
            
            <h2>关键成果</h2>
            <ul>
                <li>✅ 成功发布智能助手3.0版本</li>
                <li>📈 用户数量突破10万大关</li>
                <li>🏆 获得行业最佳创新奖</li>
                <li>💸 完成B轮融资3000万</li>
                <li>🏪 建立5个城市服务中心</li>
            </ul>
            
            <h2>下一步计划</h2>
            <ul>
                <li>📱 Q3推出移动端应用</li>
                <li>⚙️ 扩展企业级功能模块</li>
                <li>🌐 建设开发者生态</li>
                <li>🌍 进军国际市场</li>
                <li>📈 启动IPO准备工作</li>
            </ul>
            
            <p style="text-align: center; font-size: 18px; margin-top: 30px;">
                <strong>谢谢大家！</strong><br>
                联系邮箱: zhang@tech.com
            </p>
        </div>
    </body>
    </html>
    """

def test_html_to_pptx_conversion():
    """测试HTML到PPTX的转换功能"""
    print("🧪 测试1: HTML到PPTX转换")
    print("-" * 40)
    
    agent = HTML2PPTXAgent()
    html_content = create_test_html_content()
    
    # 将HTML内容保存到文件，方便查看
    os.makedirs("input", exist_ok=True)
    with open("input/test_content.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("💾 HTML内容已保存到: input/test_content.html")
    
    try:
        result = agent.html_to_pptx(
            html_content=html_content,
            output_path="output/html_to_pptx_result.pptx",
            title="HTML转PPTX测试演示",
            verbose=True
        )
        print(f"✅ HTML到PPTX转换成功: {result}")
        return True
    except Exception as e:
        print(f"❌ HTML到PPTX转换失败: {e}")
        return False

def test_html_with_images():
    """测试包含图片的HTML转换"""
    print("\n🧪 测试2: 包含图片的HTML转换")
    print("-" * 40)
    
    html_with_images = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .slide {
                padding: 20px;
                margin: 20px 0;
                border: 2px solid #28a745;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border-radius: 10px;
            }
            .slide h1 {
                color: #FFD700;
                text-align: center;
            }
            .slide img {
                max-width: 300px;
                border-radius: 8px;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="slide">
            <h1>🖼️ 图片展示页面</h1>
            <p>这是一个包含图片的测试页面</p>
            <div style="text-align: center;">
                <img src="https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Sample+Image+1" alt="示例图片1">
                <img src="https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text=Sample+Image+2" alt="示例图片2">
            </div>
            <p>图片可以很好地增强演示效果！</p>
        </div>
    </body>
    </html>
    """
    
    agent = HTML2PPTXAgent()
    
    try:
        result = agent.html_to_pptx(
            html_content=html_with_images,
            output_path="output/html_with_images_result.pptx",
            title="包含图片的HTML转PPTX测试",
            verbose=True
        )
        print(f"✅ 包含图片的HTML转换成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 包含图片的HTML转换失败: {e}")
        return False

def test_custom_template():
    """测试自定义模板转换"""
    print("\n🧪 测试3: 自定义模板转换")
    print("-" * 40)
    
    custom_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .slide {
                padding: 30px;
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                border: 3px solid #ff6b9d;
                border-radius: 15px;
                margin: 20px 0;
                color: #333;
            }
            .slide h1 {
                color: #d63384;
                font-size: 32px;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin: 15px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="slide">
            <h1>🎨 自定义样式测试</h1>
            <div class="card">
                <h2>📋 特色功能</h2>
                <ul>
                    <li>🎯 自动样式识别</li>
                    <li>🎨 渐变背景支持</li>
                    <li>💫 阴影效果保留</li>
                </ul>
            </div>
            <div class="card">
                <h2>🚀 性能优势</h2>
                <p>高效的HTML解析和PPT生成能力，支持复杂样式转换。</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    agent = HTML2PPTXAgent()
    
    try:
        result = agent.html_to_pptx(
            html_content=custom_html,
            output_path="output/custom_template_result.pptx",
            title="自定义模板测试",
            verbose=True
        )
        print(f"✅ 自定义模板转换成功: {result}")
        return True
    except Exception as e:
        print(f"❌ 自定义模板转换失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 HTML2PPTXAgent 功能测试")
    print("=" * 50)
    
    # 确保输入输出目录存在
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # 运行测试
    results = []
    results.append(test_html_to_pptx_conversion())
    results.append(test_html_with_images())
    results.append(test_custom_template())
    
    # 测试结果总结
    print("\n📊 测试结果总结")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    test_names = ["基本HTML转换", "图片HTML转换", "自定义模板转换"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n🎯 总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    print("\n📁 生成的文件:")
    for folder in ["input", "output"]:
        if os.path.exists(folder):
            print(f"\n{folder}/:")
            for file in os.listdir(folder):
                print(f"  • {file}")

if __name__ == "__main__":
    main()
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from datetime import datetime
from src.autoagentsai.client import ChatClient
from src.autoagentsai.react.create_react_agent import create_react_agent
from src.autoagentsai.tools import ToolManager, ToolWrapper, tool

# ChatClient配置
CHAT_CONFIG = {
    "agent_id": "7e46d18945fc49379063e3057a143c58",
    "personal_auth_key": "339859fa69934ea8b2b0ebd19d94d7f1",
    "personal_auth_secret": "93TsBecJplOawEipqAdF7TJ0g4IoBMtA",
    "base_url": "https://uat.agentspro.cn"
}

# ============= 定义自定义工具 =============

@tool(name="加法计算器", description="计算两个数字的和")
def add(a: int, b: int) -> int:
    """计算两个整数的和"""
    return a + b

@tool(name="乘法计算器", description="计算两个数字的乘积")
def multiply(x: float, y: float) -> float:
    """计算两个数的乘积"""
    return x * y

def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def divide(a: float, b: float) -> float:
    """除法运算，可能抛出异常"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

async def test_toolmanager_refactor():
    """测试重构后的ToolManager架构"""
    print("🔧 测试重构后的ToolManager架构")
    print("=" * 60)
    
    try:
        # 1. 创建ChatClient
        chat_client = ChatClient(
            agent_id=CHAT_CONFIG["agent_id"],
            personal_auth_key=CHAT_CONFIG["personal_auth_key"],
            personal_auth_secret=CHAT_CONFIG["personal_auth_secret"],
            base_url=CHAT_CONFIG["base_url"]
        )
        print("✅ ChatClient创建成功")
        
        # 2. 创建混合工具列表
        tools = [
            add,                                              # @tool装饰的函数
            multiply,                                         # @tool装饰的函数
            get_current_time,                                # 普通函数
            ToolWrapper(divide, "除法计算器", "执行除法运算")  # ToolWrapper包装的函数
        ]
        
        # 3. 创建React Agent（内部使用ToolManager）
        react_agent = create_react_agent(chat_client=chat_client, tools=tools)
        print(f"✅ React Agent创建成功，包含 {len(tools)} 个工具")
        print()
        
        # 4. 测试不同类型的查询
        test_queries = [
            "计算 15 + 25 的结果",                # 测试加法
            "现在是几点？",                       # 测试时间查询
            "计算 8.5 乘以 4.2",                 # 测试乘法
            "50 除以 10 等于多少？",             # 测试除法
            "什么是机器学习？"                   # 测试无需工具的查询
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 查询 {i}/{len(test_queries)}: {query}")
            print("-" * 50)
            
            try:
                # 执行查询，观察ToolManager的工作流程
                response = await react_agent.invoke(query)
                
                print("🎯 最终回答:")
                print(response)
                
            except Exception as e:
                print(f"❌ 查询失败: {e}")
            
            print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

async def test_direct_toolmanager():
    """直接测试ToolManager功能"""
    print("🛠️ 直接测试ToolManager功能")
    print("=" * 60)
    
    try:
        # 创建ChatClient
        chat_client = ChatClient(
            agent_id=CHAT_CONFIG["agent_id"],
            personal_auth_key=CHAT_CONFIG["personal_auth_key"],
            personal_auth_secret=CHAT_CONFIG["personal_auth_secret"],
            base_url=CHAT_CONFIG["base_url"]
        )
        
        # 创建工具列表
        tools = [add, multiply, get_current_time]
        
        # 直接创建ToolManager
        tool_manager = ToolManager(chat_client, tools)
        print(f"✅ ToolManager创建成功，标准化了 {len(tool_manager.tools)} 个工具")
        
        # 打印标准化后的工具信息
        print("\n📋 标准化后的工具列表:")
        for i, tool in enumerate(tool_manager.tools, 1):
            print(f"  {i}. {tool['name']} ({tool['tool_type']})")
            print(f"     描述: {tool['description']}")
        
        # 测试工具选择
        user_query = "计算 12 + 8 的结果"
        print(f"\n🎯 测试工具选择: {user_query}")
        selected_tools = await tool_manager.select_tools(user_query)
        
        if selected_tools:
            # 测试工具执行
            print(f"\n⚙️ 测试工具执行...")
            results = await tool_manager.execute_tools(selected_tools)
            
            print(f"\n📊 执行结果摘要:")
            for result in results:
                if result.get('status') == 'success':
                    print(f"  ✅ {result['tool']}: {result['result']}")
                else:
                    print(f"  ❌ {result['tool']}: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ ToolManager测试失败: {e}")

async def main():
    """主函数"""
    print("🚀 ToolManager重构测试")
    print("=" * 70)
    print("💡 测试内容:")
    print("   1. ToolManager独立模块化")
    print("   2. create_react_agent使用ToolManager")
    print("   3. 工具选择和执行结果打印")
    print("   4. 各种工具类型的支持")
    print("=" * 70)
    
    try:
        # 运行直接ToolManager测试
        await test_direct_toolmanager()
        
        print("\n" + "="*80 + "\n")
        
        # 运行完整的重构测试
        await test_toolmanager_refactor()
        
        print("\n✅ 所有重构测试完成!")
        
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断测试")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")

if __name__ == "__main__":
    print("📚 ToolManager重构功能说明:")
    print("="*50)
    print("🔧 架构改进:")
    print("  - ToolManager独立到tools包中")
    print("  - create_react_agent专注于核心逻辑")
    print("  - 工具相关功能模块化管理")
    print("  - generate方法内联到invoke中")
    print("="*50)
    
    asyncio.run(main()) 
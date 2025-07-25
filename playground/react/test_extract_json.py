import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.utils.extractor import extract_json

# 测试不同格式的JSON响应
test_cases = [
    # 案例1: ```json```代码块格式
    '''
    这是一个JSON响应：
    ```json
    {
        "selected_tools": [
            {
                "tool_name": "add",
                "arguments": {"a": 10, "b": 20},
                "reason": "用户需要进行数学计算"
            }
        ]
    }
    ```
    ''',
    
    # 案例2: 纯代码块格式
    '''
    以下是选择结果：
    ```
    {
        "selected_tools": [
            {
                "tool_name": "search",
                "arguments": {"query": "Python", "num_results": 5},
                "reason": "用户需要搜索信息"
            }
        ]
    }
    ```
    ''',
    
    # 案例3: 直接JSON格式
    '''
    {
        "selected_tools": [
            {
                "tool_name": "get_time",
                "arguments": {},
                "reason": "用户询问时间"
            }
        ]
    }
    其他文本内容
    ''',
    
    # 案例4: 带换行和空格的JSON
    '''
             {
                 "selected_tools": [
                     {
                         "tool_name": "multiply",
                         "arguments": {"x": 6, "y": 7},
                         "reason": "乘法计算"
                     }
                 ]
             }
             ''',
    
    # 案例5: MockChatClient的实际返回格式
    '''
             {
                 "selected_tools": [
                     {
                         "tool_name": "add",
                         "arguments": {"a": 10, "b": 20},
                         "reason": "用户需要进行数学计算"
                     }
                 ]
             }
             ''',
    
    # 案例6: 无效的JSON
    '''
    这不是有效的JSON：
    {invalid json content
    ''',
    
    # 案例7: 空的selected_tools
    '''
    {
        "selected_tools": []
    }
    '''
]

print("🧪 测试extract_json方法")
print("=" * 60)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n📝 测试案例 {i}:")
    print(f"输入: {repr(test_case[:100])}...")
    
    result = extract_json(test_case)
    
    if result:
        print(f"✅ 成功提取JSON:")
        print(f"   类型: {type(result)}")
        if isinstance(result, dict):
            selected_tools = result.get('selected_tools', [])
            print(f"   选择的工具数量: {len(selected_tools)}")
            for j, tool in enumerate(selected_tools):
                print(f"      工具{j+1}: {tool.get('tool_name', 'unknown')}")
        else:
            print(f"   内容: {result}")
    else:
        print(f"❌ 提取失败: {result}")

print("\n" + "=" * 60)
print("✅ extract_json测试完成")
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# 直接导入E2B模块，避免依赖问题
from src.autoagentsai.sandbox.E2B import E2BSandboxService

def test_minimal_plot():
    """测试最简单的matplotlib图片生成"""
    print("🚀 创建E2B沙箱服务...")
    sandbox = E2BSandboxService()
    
    # 最简单的matplotlib代码
    simple_plot_code = """
import matplotlib
matplotlib.use('Agg')  # 使用无GUI后端
import matplotlib.pyplot as plt

print("开始创建图片...")

# 创建最简单的图
plt.figure()
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title('Simple Plot')

# 保存图片
plt.savefig('simple.png')
print("图片已保存为 simple.png")
plt.close()
"""
    
    print("📊 执行最简单的图片生成...")
    result = sandbox.run_code(simple_plot_code)
    
    print(f"📋 执行结果: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    
    if result.get('error'):
        print(f"❗ 错误信息: {result['error']}")
    
    if result.get('output'):
        print(f"📄 输出内容:")
        for line in result['output']:
            print(f"  {line.strip()}")
    
    return result.get('success', False)

def test_even_simpler():
    """测试更简单的代码，不涉及matplotlib"""
    print("\n🔍 测试基础Python功能...")
    sandbox = E2BSandboxService()
    
    basic_code = """
print("Python基础测试")

# 测试字符串操作
text = "hello world"
print(f"文本: {text}")
print(f"文本长度: {len(text)}")

# 测试文件写入
with open('test.txt', 'w') as f:
    f.write('Hello from E2B!')

print("文件已创建")

# 测试列表推导式
numbers = [i for i in range(5)]
print(f"数字列表: {numbers}")
"""
    
    result = sandbox.run_code(basic_code)
    
    print(f"基础测试结果: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    
    if result.get('error'):
        print(f"❗ 错误信息: {result['error']}")
    
    if result.get('output'):
        print(f"📄 输出内容:")
        for line in result['output']:
            print(f"  {line.strip()}")

def test_step_by_step_plot():
    """逐步测试matplotlib的每个步骤"""
    print("\n🎯 逐步测试matplotlib...")
    sandbox = E2BSandboxService()
    
    # 步骤1：导入测试
    step1 = """
print("步骤1: 导入matplotlib")
import matplotlib
print("matplotlib导入成功")
"""
    
    result1 = sandbox.run_code(step1)
    print(f"步骤1结果: {'✅' if result1.get('success') else '❌'}")
    if result1.get('error'):
        print(f"  错误: {result1['error']}")
    
    # 步骤2：设置后端
    step2 = """
print("步骤2: 设置后端")
import matplotlib
matplotlib.use('Agg')
print("后端设置成功")
"""
    
    result2 = sandbox.run_code(step2)
    print(f"步骤2结果: {'✅' if result2.get('success') else '❌'}")
    if result2.get('error'):
        print(f"  错误: {result2['error']}")
    
    # 步骤3：导入pyplot
    step3 = """
print("步骤3: 导入pyplot")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
print("pyplot导入成功")
"""
    
    result3 = sandbox.run_code(step3)
    print(f"步骤3结果: {'✅' if result3.get('success') else '❌'}")
    if result3.get('error'):
        print(f"  错误: {result3['error']}")

if __name__ == "__main__":
    print("🧪 开始matplotlib专项测试...")
    
    try:
        test_even_simpler()
        test_step_by_step_plot()
        test_minimal_plot()
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc() 
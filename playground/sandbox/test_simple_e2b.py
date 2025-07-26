import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# 直接导入E2B模块，避免依赖问题
from src.autoagentsai.sandbox.E2B import E2BSandboxService

def test_simple_execution():
    """测试简单的代码执行功能"""
    print("🚀 创建E2B沙箱服务...")
    
    try:
        sandbox = E2BSandboxService()
        print("✅ 沙箱创建成功")
    except Exception as e:
        print(f"❌ 沙箱创建失败: {e}")
        return
    
    # 测试最简单的代码
    simple_code = """
print("Hello from E2B sandbox!")
print("测试中文输出")

# 测试基本的数学运算
result = 1 + 1
print(f"1 + 1 = {result}")

# 测试列表操作
numbers = [1, 2, 3, 4, 5]
print(f"数字列表: {numbers}")
print(f"列表长度: {len(numbers)}")
print(f"列表总和: {sum(numbers)}")
"""
    
    print("📊 执行简单代码测试...")
    result = sandbox.run_code(simple_code)
    
    print(f"\n📋 执行结果: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    
    if result.get('error'):
        print(f"❗ 错误信息: {result['error']}")
    
    if result.get('output'):
        print(f"📄 输出内容:")
        print(result['output'])
    
    return result.get('success', False)

def test_pandas_basic():
    """测试pandas基本功能"""
    print("\n📊 测试pandas基本功能...")
    
    sandbox = E2BSandboxService()
    
    pandas_code = """
import pandas as pd
import numpy as np

# 创建简单的DataFrame
data = {
    'name': ['张三', '李四', '王五'],
    'age': [25, 30, 35], 
    'salary': [5000, 6000, 7000]
}

df = pd.DataFrame(data)
print("创建的DataFrame:")
print(df)
print(f"\\n数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print(f"数据类型:\\n{df.dtypes}")
"""
    
    result = sandbox.run_code(pandas_code)
    
    print(f"pandas测试结果: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    
    if result.get('error'):
        print(f"❗ 错误信息: {result['error']}")
    
    if result.get('output'):
        print(f"📄 输出内容:")
        print(result['output'])
    
    return result.get('success', False)

def test_file_operations():
    """测试文件操作"""
    print("\n📁 测试文件操作...")
    
    sandbox = E2BSandboxService()
    
    # 先上传测试文件
    try:
        csv_path = "playground/test_workspace/data.csv"
        with open(csv_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 上传到沙箱
        uploaded_file = sandbox.sandbox.files.write("test_data.csv", file_content)
        print(f"✅ 文件上传成功: {uploaded_file.path}")
        
        # 测试读取文件
        file_test_code = f"""
import pandas as pd

# 读取上传的CSV文件
df = pd.read_csv('{uploaded_file.path}')

print("文件读取成功!")
print(f"数据形状: {{df.shape}}")
print(f"列名: {{df.columns.tolist()}}")
print("前3行数据:")
print(df.head(3))
"""
        
        result = sandbox.run_code(file_test_code)
        
        print(f"文件操作测试: {'✅ 成功' if result.get('success') else '❌ 失败'}")
        
        if result.get('error'):
            print(f"❗ 错误信息: {result['error']}")
        
        if result.get('output'):
            print(f"📄 输出内容:")
            print(result['output'])
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ 文件操作失败: {e}")
        return False

def test_download_functionality():
    """测试图片下载功能"""
    print("\n📸 测试图片下载功能...")
    
    sandbox = E2BSandboxService()
    
    # 创建一个简单的图片
    plot_code = """
import matplotlib.pyplot as plt
import numpy as np

# 创建简单的图表
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('简单的正弦波')
plt.legend()
plt.grid(True)

# 保存图片
plt.savefig('simple_plot.png', dpi=300, bbox_inches='tight')
plt.close()

print("图片已保存为 simple_plot.png")
"""
    
    result = sandbox.run_code(plot_code)
    
    if result.get('success'):
        print("✅ 图片生成成功")
        
        # 测试下载
        download_result = sandbox.download_images_to_local("./downloaded_images")
        
        if download_result['success']:
            print(f"✅ 图片下载成功: {download_result['count']} 张图片")
            for file_path in download_result['downloaded_files']:
                print(f"   📁 {file_path}")
        else:
            print(f"❌ 图片下载失败: {download_result.get('error')}")
    else:
        print(f"❌ 图片生成失败: {result.get('error')}")

if __name__ == "__main__":
    print("🧪 开始E2B沙箱测试...")
    
    try:
        # 逐步测试各个功能
        success1 = test_simple_execution()
        success2 = test_pandas_basic()
        success3 = test_file_operations()
        test_download_functionality()
        
        print(f"\n📊 测试总结:")
        print(f"  基本执行: {'✅' if success1 else '❌'}")
        print(f"  Pandas测试: {'✅' if success2 else '❌'}")
        print(f"  文件操作: {'✅' if success3 else '❌'}")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc() 
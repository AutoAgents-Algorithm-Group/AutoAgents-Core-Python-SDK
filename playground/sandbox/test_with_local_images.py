import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.sandbox import E2BSandboxService

def main():
    # 创建sandbox实例
    sandbox = E2BSandboxService()
    
    # 分析CSV数据
    print("开始分析CSV数据...")
    result = sandbox.analyze_csv(
        user_query="请帮我进行全面的数据分析，包括数据概览、分布分析、相关性分析等，并生成可视化图表", 
        file_path="playground/test_workspace/data.csv"
    )
    
    print(f"\n执行结果: {'成功' if result.get('success') else '失败'}")
    
    if result.get('error'):
        print(f"错误信息: {result['error']}")
    
    if result.get('output'):
        print(f"输出信息: {result['output']}")
    
    # 显示图片信息
    if result.get('images'):
        print(f"\n在沙箱中生成了 {len(result['images'])} 张图片")
        for i, img in enumerate(result['images']):
            print(f"  图片 {i+1}: {img.get('name', f'image_{i+1}.png')} (格式: {img.get('format', 'png')})")
    
    # 显示本地下载的图片
    if result.get('local_images'):
        local_info = result['local_images']
        if local_info.get('success'):
            print(f"\n成功下载 {local_info['count']} 张图片到本地目录: {local_info['local_dir']}")
            for file_path in local_info['downloaded_files']:
                print(f"  本地文件: {file_path}")
        else:
            print(f"\n下载图片失败: {local_info.get('error')}")
    
    # 手动下载图片（如果需要自定义目录）
    print(f"\n手动下载图片到自定义目录...")
    custom_download = sandbox.download_images_to_local("./my_charts")
    if custom_download['success']:
        print(f"成功下载 {custom_download['count']} 张图片到 {custom_download['local_dir']}")
        for file_path in custom_download['downloaded_files']:
            print(f"  自定义目录文件: {file_path}")
    else:
        print(f"自定义下载失败: {custom_download.get('error')}")

if __name__ == "__main__":
    main() 
import os
import pandas as pd
from openpyxl import load_workbook

def excel_to_csv_and_images(input_file, output_csv, img_dir):
    """
    将Excel转换为CSV，并提取其中的所有图片到指定文件夹
    Args:
        input_file (str): Excel文件路径
        output_csv (str): 输出CSV路径
        img_dir (str): 输出图片文件夹路径
    """
    # 1. 读取Excel数据 → CSV
    df = pd.read_excel(input_file)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"✅ CSV 已保存：{output_csv}")

    # 2. 提取图片
    os.makedirs(img_dir, exist_ok=True)
    wb = load_workbook(input_file, data_only=True)
    ws = wb.active

    img_count = 0
    for img in ws._images:  # openpyxl 存储图片在 ws._images
        img_count += 1
        img_name = f"img_{img_count}.png"  # 统一保存为png
        img_path = os.path.join(img_dir, img_name)
        with open(img_path, "wb") as f:
            f.write(img._data())  # 直接写入图像二进制数据
    print(f"✅ 已提取 {img_count} 张图片到：{img_dir}")
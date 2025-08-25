# Slide Agent 测试文件

这个目录包含了两个核心Agent的测试文件，用于验证PPT处理功能。

## 📁 目录结构

```
playground/slide/
├── input/                          # 输入文件夹
│   ├── test_template.pptx          # PPTX模板文件
│   └── test_content.html           # HTML内容文件（运行测试时生成）
├── output/                         # 输出文件夹（测试结果）
├── test_pptx2pptx_agent.py         # PPTX2PPTXAgent测试
├── test_html2pptx_agent.py         # HTML2PPTXAgent测试
└── README.md                       # 说明文档
```

## 🧪 测试文件说明

### 1. test_pptx2pptx_agent.py
测试 **PPTX模板填充和重排序** 功能：
- ✅ 基本数据填充（保持原始顺序）
- ✅ 动态重排序填充（自定义页面顺序）
- ✅ Base64输出格式
- ✅ 多数据填充（同一模板页面填入不同内容）
- ✅ 完整的样式保留

**运行方法：**
```bash
cd playground/slide
python test_pptx2pptx_agent.py
```

### 2. test_html2pptx_agent.py
测试 **HTML到PPTX转换** 功能：
- ✅ 基本HTML内容转换
- ✅ 包含图片的HTML转换
- ✅ 自定义样式模板转换
- ✅ 样式识别和保留

**运行方法：**
```bash
cd playground/slide
python test_html2pptx_agent.py
```

### 3. test_multiple_data_fill.py
测试 **多数据填充专项功能**：
- ✅ 学生成绩单批量生成
- ✅ 产品目录批量生成
- ✅ Base64输出格式
- ✅ 自定义模板演示
- ✅ 同一模板页面，不同内容填充

**运行方法：**
```bash
cd playground/slide
python test_multiple_data_fill.py
```

**核心功能：**
使用 `fill_multiple_data()` 方法，可以将同一个模板页面复制多次，每次填入不同的数据，适用于：
- 批量生成个人资料/简历
- 批量生成产品介绍页面
- 批量生成学生成绩单/报告卡
- 批量生成员工档案
- 批量生成证书/奖状

## 📊 测试数据

### PPTX2PPTXAgent 测试数据
- 完整的商业演示数据结构
- 包含公司信息、产品介绍、财务数据
- 支持图片、表格、列表等多种内容类型
- 演示动态重排序功能

### HTML2PPTXAgent 测试数据
- 多页面HTML演示内容
- 包含渐变背景、样式效果
- 图片和复杂布局支持
- 自定义CSS样式测试

## 🎯 预期输出

运行测试后，`output/` 文件夹将包含：

**PPTX2PPTXAgent输出：**
- `basic_fill_result.pptx` - 基本填充结果
- `reorder_fill_result.pptx` - 重排序填充结果
- `base64_result.txt` - Base64格式输出

**HTML2PPTXAgent输出：**
- `html_to_pptx_result.pptx` - 基本HTML转换结果
- `html_with_images_result.pptx` - 包含图片的转换结果
- `custom_template_result.pptx` - 自定义模板转换结果

## 💡 使用提示

1. **确保模板存在**：`input/test_template.pptx` 需要存在才能运行PPTX2PPTXAgent测试
2. **网络连接**：某些测试使用在线图片，需要网络连接
3. **输出目录**：测试会自动创建`output/`目录
4. **错误排查**：查看测试输出的详细信息来诊断问题

## 🔧 自定义测试

可以修改测试文件中的数据和配置来测试不同场景：
- 修改 `create_test_data()` 函数来测试不同的数据结构
- 调整 `order_info` 配置来测试不同的重排序方案
- 修改HTML内容来测试不同的样式效果

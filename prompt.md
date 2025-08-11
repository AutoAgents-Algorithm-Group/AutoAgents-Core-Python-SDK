# 动态PPT内容生成器使用指南

## 🚀 快速开始

动态PPT内容生成器 (`DynamicSlideAgent`) 可以根据您的需求自动生成符合占位符规则的PPT内容JSON结构。

### 基本使用

```python
from src.autoagentsai.slide import DynamicSlideAgent

# 创建生成器
generator = DynamicSlideAgent()

# 生成PPT内容
result = generator.generate_slide_content(
    user_request="创建一个关于AI技术的商业演示PPT，包含6页内容",
    pages_count=6,
    include_images=True,
    include_tables=True
)

# 保存结果
generator.export_to_json_file(result, "my_ppt.json")
```

## 📋 占位符规则

| 类型 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 文本 | `{{path}}` | `{{page[0].title}}` | 普通文本、Markdown、列表 |
| 图片 | `{{@path}}` | `{{@page[0].logo}}` | 本地路径或远程URL |
| 表格 | `{{#path}}` | `{{#page[1].table}}` | CSV文件或JSON数组 |

## 🎯 模板类型

- `business` - 商业演示
- `technology` - 技术分享  
- `education` - 教育培训
- `product` - 产品发布
- `report` - 工作汇报

## 📁 文件说明

- `DynamicSlideAgent.py` - 核心生成器类
- `test_dynamic_generator.py` - 完整测试示例
- `quick_generator_example.py` - 快速使用示例
- `ppt_prompt_templates.md` - 详细提示词模板指南

## 💡 使用流程

1. 使用 `DynamicSlideAgent` 生成JSON内容
2. 在PPT模板中放置占位符
3. 使用 `SlideAgent.fill()` 填充内容
4. 生成最终PPT文件

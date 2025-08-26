# AutoAgents Slide Module

AutoAgents的幻灯片处理模块，提供强大的PowerPoint文档生成和填充功能。

## 📋 目录

- [模块概述](#模块概述)
- [主要特性](#主要特性)
- [快速开始](#快速开始)
- [核心组件](#核心组件)
- [使用方法](#使用方法)
- [API文档](#api文档)
- [示例代码](#示例代码)
- [目录结构](#目录结构)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 🎯 模块概述

AutoAgents Slide模块是一个专业的PowerPoint文档处理工具集，支持：

- **PPTX模板填充** - 使用JSON数据填充PowerPoint模板
- **HTML转PPTX** - 将HTML内容转换为PowerPoint演示文稿
- **动态幻灯片生成** - 根据数据动态创建和排序幻灯片
- **多种数据格式支持** - 文本、图片、表格、列表等
- **智能错误处理** - 自动跳过问题形状，确保程序稳定运行

## ✨ 主要特性

### 🔧 PPTX2PPTXAgent

- **双模式支持**
  - 📄 传统填充模式：直接填充模板所有占位符
  - 🎯 渲染指令模式：自定义幻灯片顺序和内容选择

- **丰富的占位符类型**
  - `{{key}}` - 文本占位符
  - `{{@key}}` - 图片占位符
  - `{{#key}}` - 表格占位符

- **高级数据访问**
  - 嵌套路径：`{{user.profile.name}}`
  - 数组索引：`{{items[0].title}}`
  - 复合路径：`{{users[1].posts[0].content}}`

- **稳定的错误处理**
  - 自动跳过组合形状（避免lxml错误）
  - 异常保护机制
  - 详细的错误日志

### 🌐 HTML2PPTXAgent

- HTML内容解析和转换
- 自动样式映射
- 多页面HTML支持
- 智能内容提取

### 📊 SlideAgent

- 基础幻灯片处理功能
- 统一的接口设计
- 可扩展的架构

## 🚀 快速开始

### 安装依赖

```bash
pip install python-pptx requests pillow beautifulsoup4
```

### 基本使用

```python
from src.autoagentsai.slide import PPTX2PPTXAgent

# 创建代理实例
agent = PPTX2PPTXAgent()

# 准备数据
data = {
    "presentation": {
        "title": "我的演示文稿",
        "subtitle": "自动生成的PowerPoint",
        "date": "2024年12月"
    },
    "company": {
        "name": "科技公司",
        "description": "我们专注于AI和大数据解决方案"
    }
}

# 填充模板
result = agent.fill(
    data=data,
    template_file_path="input/template.pptx",
    output_file_path="output/result.pptx"
)
```

## 🧩 核心组件

### PPTX2PPTXAgent

PowerPoint模板填充的核心组件，支持复杂的数据结构和动态内容生成。

**主要方法：**
- `fill()` - 填充模板的主要方法
- `_is_safe_shape()` - 形状安全检查
- `_render_slides_from_instructions()` - 渲染指令处理

### HTML2PPTXAgent

HTML到PowerPoint的转换工具，适合从网页内容生成演示文稿。

### SlideAgent

提供基础的幻灯片处理功能和统一接口。

## 📖 使用方法

### 1. 传统填充模式

直接填充模板中的所有占位符，保持原有幻灯片顺序。

```python
agent = PPTX2PPTXAgent()

data = {
    "presentation": {"title": "年度报告", "date": "2024"},
    "company": {"name": "创新科技", "revenue": "1亿元"}
}

# 不传递order_info参数
result = agent.fill(
    data=data,
    template_file_path="template.pptx",
    output_file_path="output.pptx"
)
```

### 2. 渲染指令模式

使用渲染指令自定义幻灯片的顺序和内容选择。

```python
agent = PPTX2PPTXAgent()

data = {
    "cover": {"title": "项目汇报", "author": "张经理"},
    "achievements": [
        {"title": "A轮融资", "desc": "获得5000万投资"},
        {"title": "用户增长", "desc": "突破100万用户"}
    ],
    "plans": {"focus": "AI产品研发"}
}

# 定义渲染指令
render_instructions = [
    (0, "cover"),           # 幻灯片0：封面
    (1, "achievements[0]"), # 幻灯片1：第一个成就
    (1, "achievements[1]"), # 幻灯片1：第二个成就（重复使用模板）
    (2, "plans")            # 幻灯片2：未来计划
]

result = agent.fill(
    data=data,
    template_file_path="template.pptx",
    output_file_path="output.pptx",
    order_info=render_instructions  # 关键参数
)
```

### 3. 多种输出格式

```python
# 本地文件输出（默认）
result = agent.fill(data, template_path, output_path="local.pptx")

# Base64编码输出
result = agent.fill(data, template_path, output_format="base64")

# 上传到服务器
result = agent.fill(
    data, template_path, 
    output_format="url",
    personal_auth_key="your_key",
    personal_auth_secret="your_secret"
)
```

## 📚 API文档

### PPTX2PPTXAgent.fill()

```python
def fill(self,
         data: dict,
         template_file_path: str,
         output_file_path: Optional[str] = None,
         output_format: str = "local",
         personal_auth_key: Optional[str] = None,
         personal_auth_secret: Optional[str] = None,
         base_url: str = "https://uat.agentspro.cn",
         order_info: Optional[List[tuple]] = None,
         verbose: bool = True) -> Union[str, Dict]:
```

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `data` | `dict` | 要填充的数据字典，支持嵌套结构 |
| `template_file_path` | `str` | 模板文件路径（本地路径或URL） |
| `output_file_path` | `Optional[str]` | 输出文件路径（local格式时必需） |
| `output_format` | `str` | 输出格式："local", "base64", "url" |
| `personal_auth_key` | `Optional[str]` | 个人认证密钥（url格式时需要） |
| `personal_auth_secret` | `Optional[str]` | 个人认证密钥（url格式时需要） |
| `base_url` | `str` | 上传服务的基础URL |
| `order_info` | `Optional[List[tuple]]` | 渲染指令列表 |
| `verbose` | `bool` | 是否显示详细输出信息 |

**返回值：**
- `str` - 本地文件路径或Base64字符串
- `Dict` - 上传结果字典（url格式时）

### 占位符格式

| 格式 | 用途 | 示例 |
|------|------|------|
| `{{key}}` | 文本内容 | `{{presentation.title}}` |
| `{{@key}}` | 图片URL/路径 | `{{@company.logo}}` |
| `{{#key}}` | 表格数据 | `{{#financial_data}}` |

### 数据路径示例

```python
data = {
    "user": {
        "name": "张三",
        "posts": [
            {"title": "第一篇文章", "content": "内容1"},
            {"title": "第二篇文章", "content": "内容2"}
        ]
    },
    "company": {
        "departments": [
            {"name": "技术部", "count": 50},
            {"name": "市场部", "count": 30}
        ]
    }
}

# 支持的路径访问：
# {{user.name}} → "张三"
# {{user.posts[0].title}} → "第一篇文章"
# {{company.departments[1].name}} → "市场部"
```

## 🔧 示例代码

### 完整示例：企业年报生成

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.autoagentsai.slide.pptx2pptx_agent import PPTX2PPTXAgent

def generate_annual_report():
    """生成企业年报PPT"""
    
    agent = PPTX2PPTXAgent()
    
    # 年报数据
    annual_data = {
        "cover": {
            "title": "2024年度工作总结",
            "subtitle": "创新驱动，共创未来",
            "author": "董事会",
            "date": "2024年12月"
        },
        "achievements": [
            {
                "title": "营收突破",
                "desc": "全年营收达到10亿元，同比增长35%",
                "details": "• 核心业务增长50%\n• 新业务贡献25%\n• 海外市场贡献15%"
            },
            {
                "title": "技术创新",
                "desc": "完成15项核心技术专利申请",
                "details": "• AI算法优化\n• 大数据平台升级\n• 云原生架构迁移"
            }
        ],
        "challenges": [
            {
                "title": "市场竞争",
                "desc": "行业竞争加剧，需要差异化策略",
                "solutions": "• 加强技术研发\n• 提升服务质量\n• 拓展新市场"
            }
        ],
        "future_plans": {
            "focus": "全面推进数字化转型战略",
            "key_initiatives": [
                "建设AI研发中心",
                "启动国际化进程", 
                "推出新一代产品",
                "加强人才引进"
            ],
            "investments": "研发投入2亿元，市场拓展1亿元"
        }
    }
    
    # 渲染指令：自定义幻灯片顺序
    render_instructions = [
        (0, "cover"),            # 封面页
        (1, "achievements[0]"),  # 第一个成就
        (1, "achievements[1]"),  # 第二个成就
        (2, "challenges[0]"),    # 挑战分析
        (3, "future_plans")      # 未来规划
    ]
    
    try:
        result = agent.fill(
            data=annual_data,
            template_file_path="input/annual_report_template.pptx",
            output_file_path="output/annual_report_2024.pptx",
            order_info=render_instructions,
            verbose=True
        )
        
        print(f"✅ 年报生成成功: {result}")
        return result
        
    except Exception as e:
        print(f"❌ 年报生成失败: {e}")
        return None

if __name__ == "__main__":
    generate_annual_report()
```

### 表格数据填充示例

```python
def generate_sales_report():
    """生成销售报表"""
    
    agent = PPTX2PPTXAgent()
    
    # 包含表格数据的销售报表
    sales_data = {
        "report_title": "Q4销售业绩报告",
        "quarterly_sales": [  # 表格数据
            {"产品": "AI平台", "Q1": "1000万", "Q2": "1200万", "Q3": "1500万", "Q4": "1800万"},
            {"产品": "数据服务", "Q1": "800万", "Q2": "900万", "Q3": "1100万", "Q4": "1300万"},
            {"产品": "咨询服务", "Q1": "500万", "Q2": "600万", "Q3": "700万", "Q4": "900万"}
        ],
        "summary": {
            "total_revenue": "6.2亿元",
            "growth_rate": "45%",
            "top_product": "AI平台"
        }
    }
    
    # 模板中使用 {{#quarterly_sales}} 表格占位符
    result = agent.fill(
        data=sales_data,
        template_file_path="input/sales_template.pptx",
        output_file_path="output/q4_sales_report.pptx"
    )
    
    return result
```

### 图片和多媒体内容

```python
def generate_product_showcase():
    """生成产品展示PPT"""
    
    data = {
        "product": {
            "name": "智能分析平台",
            "logo": "https://example.com/logo.png",  # 图片URL
            "screenshot": "/local/path/screenshot.jpg",  # 本地图片
            "features": [
                "实时数据处理",
                "智能预测分析", 
                "可视化报表",
                "API集成"
            ]
        }
    }
    
    # 模板中使用：
    # {{product.name}} - 文本
    # {{@product.logo}} - 图片
    # {{@product.screenshot}} - 图片
    
    result = agent.fill(
        data=data,
        template_file_path="input/product_template.pptx",
        output_file_path="output/product_showcase.pptx"
    )
    
    return result
```

## 📁 目录结构

```
playground/slide/
├── README.md                    # 本文档
├── input/                       # 模板文件目录
│   ├── test_template_with_order_info.pptx
│   └── test_template_wo_order_info.pptx
├── output/                      # 输出文件目录
│   └── (生成的PPTX文件)
├── test_pptx2pptx_agent.py     # PPTX代理测试
└── test_html2pptx_agent.py     # HTML代理测试

src/autoagentsai/slide/
├── __init__.py                  # 模块初始化
├── SlideAgent.py               # 基础幻灯片代理
├── pptx2pptx_agent.py          # PPTX填充代理
└── html2pptx_agent.py          # HTML转换代理
```

## 💡 最佳实践

### 1. 数据结构设计

**推荐的数据结构：**
```python
# ✅ 良好的结构
data = {
    "cover": {"title": "...", "author": "..."},
    "content": [
        {"title": "...", "description": "..."},
        {"title": "...", "description": "..."}
    ],
    "summary": {"key_points": [...]}
}

# ❌ 避免的结构
data = {
    "data1": "...",
    "data2": "...",
    "data3": "..."
}
```

### 2. 模板设计原则

- **占位符命名**：使用有意义的名称，如`{{company.name}}`而不是`{{data1}}`
- **布局一致性**：保持模板布局的一致性，便于批量处理
- **类型标识**：明确区分文本、图片、表格占位符

### 3. 错误处理

```python
try:
    result = agent.fill(
        data=data,
        template_file_path=template_path,
        output_file_path=output_path,
        verbose=True  # 开启详细日志
    )
    print(f"成功生成: {result}")
except Exception as e:
    print(f"生成失败: {e}")
    # 记录错误日志或进行其他处理
```

### 4. 性能优化

- **图片优化**：使用适当分辨率的图片，避免过大文件
- **数据预处理**：在调用`fill()`前预处理和验证数据
- **模板复用**：设计可复用的模板结构

### 5. 批量处理

```python
def batch_generate_reports(data_list, template_path):
    """批量生成报告"""
    agent = PPTX2PPTXAgent()
    results = []
    
    for i, data in enumerate(data_list):
        try:
            output_path = f"output/report_{i+1}.pptx"
            result = agent.fill(
                data=data,
                template_file_path=template_path,
                output_file_path=output_path,
                verbose=False  # 批量处理时关闭详细日志
            )
            results.append(result)
        except Exception as e:
            print(f"第{i+1}个报告生成失败: {e}")
            results.append(None)
    
    return results
```

## ❓ 常见问题

### Q1: 如何处理中文字符？

**A:** 模块完全支持中文字符，确保：
- 数据使用UTF-8编码
- 模板文件支持中文字体
- 文件路径不包含特殊字符

### Q2: 支持哪些图片格式？

**A:** 支持常见图片格式：
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.svg`
- 支持本地路径和HTTP/HTTPS URL

### Q3: 如何处理大量数据？

**A:** 对于大量数据：
- 使用渲染指令模式选择性生成内容
- 分批处理，避免内存占用过高
- 使用`verbose=False`减少日志输出

### Q4: 模板设计有什么限制？

**A:** 注意事项：
- 避免过多嵌套的组合形状
- 占位符应使用标准文本框
- 表格结构应保持简洁

### Q5: 如何调试模板填充问题？

**A:** 调试建议：
- 设置`verbose=True`查看详细日志
- 检查数据路径是否正确
- 验证模板中的占位符格式
- 使用简单数据先测试

### Q6: 程序遇到错误会崩溃吗？

**A:** 不会，模块包含完善的错误处理：
- 自动跳过组合形状（避免lxml错误）
- 异常形状保护机制
- 详细的错误信息和跳过日志
- 程序继续处理其他内容

## 🔗 相关链接

- [AutoAgents 主项目](../../README.md)
- [python-pptx 文档](https://python-pptx.readthedocs.io/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## 📧 支持与反馈

如有问题或建议，请提交Issue或联系开发团队。

---

**AutoAgents Slide Module** - 让PowerPoint生成更智能、更简单！ 🚀

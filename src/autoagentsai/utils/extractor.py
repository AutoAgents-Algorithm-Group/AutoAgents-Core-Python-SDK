import re
import json

def extract_json(text: str | None = None):
    """从AI响应中提取JSON内容，处理各种格式情况"""
    if not text:
        return None

    json_pattern = r'```json\s*(.*?)\s*```'
    match = re.search(json_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    return None

def extract_python_code(text: str | None = None):
    """从AI响应中提取Python代码"""
    if not text:
        return None

    python_pattern = r'```python\s*(.*?)\s*```'
    match = re.search(python_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_html(text: str | None = None):
    """从AI响应中提取HTML代码"""
    if not text:
        return None

    html_pattern = r'```html\s*(.*?)\s*```'
    match = re.search(html_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_react_code(text: str | None = None):
    """从AI响应中提取React代码"""
    if not text:
        return None

    patterns = [
        r'```react\s*\n?([\s\S]*?)\n?```',
        r'```tsx\s*\n?([\s\S]*?)\n?```',
        r'```jsx\s*\n?([\s\S]*?)\n?```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            code = match.group(1).strip()
            return code
    return None
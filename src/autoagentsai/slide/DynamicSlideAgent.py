from ..client import ChatClient
from ..utils.extractor import extract_json
from typing import List, Dict, Any, Optional
import json


class DynamicSlideAgent:
    """
    动态PPT内容生成器Agent
    
    能够根据用户输入动态生成符合占位符规则的PPT内容结构，
    支持文本、图片、表格等多种内容类型的动态生成。
    """
    
    def __init__(self, 
                 agent_id: str = "045c418f0dcf4adbb2f15031f06694d1",
                 personal_auth_key: str = "48cf18e0e0ca4b51bbf8fa60193ffb5c", 
                 personal_auth_secret: str = "HWlQXZ5vxgrXDGEtTGGdsTFhJfr9rCmD",
                 base_url: str = "https://uat.agentspro.cn"):
        """
        初始化动态PPT生成器
        
        Args:
            agent_id: AI Agent ID
            personal_auth_key: 认证密钥
            personal_auth_secret: 认证密码
            base_url: API基础URL
        """
        self.chat_client = ChatClient(
            agent_id=agent_id,
            personal_auth_key=personal_auth_key,
            personal_auth_secret=personal_auth_secret,
            base_url=base_url
        )
        
        # 占位符规则模板
        self.placeholder_rules = """
占位符使用规则：
1. 文本占位符：{{path}} - 用于普通文本、Markdown文本、列表内容
2. 图片占位符：{{@path}} - 用于本地图片路径或远程URL  
3. 表格占位符：{{#path}} - 用于CSV文件路径或JSON数组数据

示例：
- {{page[0].title}} - 获取第1页标题
- {{page[1].sections[0].content}} - 获取第2页第1个章节内容  
- {{@page[0].logo}} - 图片占位符，会替换为图片
- {{#page[1].table}} - 表格占位符，填充CSV或JSON表格数据
"""

    def _create_generation_prompt(self, user_request: str, pages_count: int = None, 
                                  include_images: bool = True, include_tables: bool = True) -> str:
        """
        创建用于生成PPT内容的提示词
        
        Args:
            user_request: 用户的PPT需求描述
            pages_count: 建议的页数（可选）
            include_images: 是否包含图片
            include_tables: 是否包含表格
            
        Returns:
            完整的提示词字符串
        """
        
        prompt = f"""你是一个专业的PPT内容生成专家。请根据用户需求生成符合以下格式的PPT内容JSON结构。

用户需求：{user_request}

{self.placeholder_rules}

请生成一个包含"page"数组的JSON结构，每个页面对象可以包含以下字段：
- page_number: 页码（数字）
- title: 页面标题（字符串）
- subtitle: 页面副标题（字符串，可选）
- logo: 图片路径（字符串，可选）
- sections: 章节数组，每个章节包含title和content字段
- table: 表格数据，可以是CSV文件路径字符串或JSON数组
- content: 页面主要内容（字符串，可选）

生成要求：
1. 内容要丰富、专业、有逻辑性
2. 如果涉及数据展示，请创建合理的表格数据
3. 图片路径使用合理的文件名（如：logo.png, chart.jpg等）
4. Markdown格式的文本请使用适当的标记（*, #, `等）
5. 确保JSON格式正确，可以直接解析"""

        if pages_count:
            prompt += f"\n6. 生成大约{pages_count}页内容"
            
        if not include_images:
            prompt += "\n7. 不要包含图片相关字段"
            
        if not include_tables:
            prompt += "\n8. 不要包含表格相关字段"

        prompt += """

参考示例结构（请根据用户需求调整内容）：
{
    "page": [
        {
            "page_number": 1,
            "title": "标题页",
            "subtitle": "副标题",
            "logo": "company_logo.png"
        },
        {
            "page_number": 2,
            "title": "章节页面",
            "sections": [
                {
                    "title": "章节标题",
                    "content": "章节内容，支持**粗体**、*斜体*、`代码`等Markdown格式"
                }
            ]
        },
        {
            "page_number": 3,
            "title": "数据展示",
            "table": [
                {
                    "name": "项目名称",
                    "value": "数值",
                    "description": "说明"
                }
            ]
        }
    ]
}

请直接返回JSON格式的数据，不要包含其他说明文字。"""

        return prompt

    def generate_slide_content(self, 
                             user_request: str,
                             pages_count: Optional[int] = None,
                             include_images: bool = True,
                             include_tables: bool = True,
                             reference_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        根据用户需求动态生成PPT内容
        
        Args:
            user_request: 用户的PPT需求描述
            pages_count: 建议的页数
            include_images: 是否包含图片占位符
            include_tables: 是否包含表格占位符  
            reference_files: 参考文件路径列表（可选）
            
        Returns:
            生成的PPT内容JSON结构
        """
        
        print(f"正在生成PPT内容：{user_request}")
        
        # 创建生成提示词
        prompt = self._create_generation_prompt(
            user_request=user_request,
            pages_count=pages_count,
            include_images=include_images,
            include_tables=include_tables
        )
        
        print("开始调用AI生成内容...")
        
        content = ""
        try:
            # 调用AI生成内容
            for event in self.chat_client.invoke(prompt, files=reference_files or []):
                if event['type'] == 'start_bubble':
                    print(f"\n{'=' * 20} 开始生成 {'=' * 20}")
                elif event['type'] == 'token':
                    print(event['content'], end='', flush=True)
                    content += event['content']
                elif event['type'] == 'end_bubble':
                    print(f"\n{'=' * 20} 生成完成 {'=' * 20}")
                elif event['type'] == 'finish':
                    print(f"\n{'=' * 20} 任务完成 {'=' * 20}")
                    break
                elif event['type'] == 'error':
                    print(f"\n错误: {event}")
                    break
                    
        except Exception as e:
            print(f"\n生成过程中发生错误: {type(e).__name__}: {e}")
            if not content.strip():
                content = f"生成错误: {str(e)}"
        
        print(f"\n生成内容长度: {len(content)}")
        
        # 提取JSON内容
        try:
            result = extract_json(content)
            if result and isinstance(result, dict) and 'page' in result:
                print(f"成功生成 {len(result['page'])} 页PPT内容")
                return result
            else:
                print("生成的内容格式不正确，尝试手动解析...")
                # 尝试直接解析JSON
                json_content = content.strip()
                if json_content.startswith('```json'):
                    json_content = json_content[7:]
                if json_content.endswith('```'):
                    json_content = json_content[:-3]
                return json.loads(json_content.strip())
                
        except Exception as e:
            print(f"JSON解析失败: {e}")
            print(f"原始内容: {content[:500]}...")
            return {"error": f"解析失败: {str(e)}", "raw_content": content}

    def generate_with_template(self, 
                             template_type: str,
                             custom_data: Dict[str, Any],
                             pages_count: Optional[int] = None) -> Dict[str, Any]:
        """
        基于模板类型和自定义数据生成PPT内容
        
        Args:
            template_type: 模板类型（如：business, education, technology等）
            custom_data: 自定义数据字典
            pages_count: 页数
            
        Returns:
            生成的PPT内容JSON结构
        """
        
        template_prompts = {
            "business": "创建一个商业演示PPT，包含公司介绍、产品/服务、市场分析、财务数据等内容",
            "education": "创建一个教育培训PPT，包含课程目标、知识点、案例分析、练习题等内容", 
            "technology": "创建一个技术分享PPT，包含技术介绍、架构图、代码示例、最佳实践等内容",
            "product": "创建一个产品发布PPT，包含产品特性、竞争优势、用户反馈、发展路线图等内容",
            "report": "创建一个工作汇报PPT，包含项目进展、数据分析、问题总结、下一步计划等内容"
        }
        
        base_prompt = template_prompts.get(template_type, template_prompts["business"])
        
        # 将自定义数据融入提示词
        data_context = "请结合以下信息生成内容：\n"
        for key, value in custom_data.items():
            data_context += f"- {key}: {value}\n"
            
        full_request = f"{base_prompt}\n\n{data_context}"
        
        return self.generate_slide_content(
            user_request=full_request,
            pages_count=pages_count,
            include_images=True,
            include_tables=True
        )

    def validate_slide_structure(self, slide_data: Dict[str, Any]) -> bool:
        """
        验证生成的PPT结构是否符合要求
        
        Args:
            slide_data: PPT数据结构
            
        Returns:
            是否有效
        """
        
        if not isinstance(slide_data, dict):
            return False
            
        if 'page' not in slide_data:
            return False
            
        pages = slide_data['page']
        if not isinstance(pages, list) or len(pages) == 0:
            return False
            
        for page in pages:
            if not isinstance(page, dict):
                return False
            if 'page_number' not in page or 'title' not in page:
                return False
                
        return True

    def export_to_json_file(self, slide_data: Dict[str, Any], output_path: str) -> bool:
        """
        将生成的PPT数据导出为JSON文件
        
        Args:
            slide_data: PPT数据结构
            output_path: 输出文件路径
            
        Returns:
            是否导出成功
        """
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(slide_data, f, ensure_ascii=False, indent=2)
            print(f"PPT数据已导出到: {output_path}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
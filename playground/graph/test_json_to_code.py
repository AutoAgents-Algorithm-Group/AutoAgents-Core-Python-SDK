import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagentsai.graph import FlowGraph

def main():
    # 你提供的JSON数据
    json_data = {
        "nodes": [
            {
                "id": "simpleInputId",
                "type": "custom",
                "initialized": False,
                "position": {"x": 0, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "description": "引用变量：{{userChatInput}}", "label": "文本信息", "type": "source", "targets": [], "key": "userChatInput"},
                        {"valueType": "file", "description": "以JSON数组格式输出用户上传文档列表，若为文档比对，包含分组信息", "label": "文档信息", "type": "source", "targets": [], "key": "files"},
                        {"valueType": "image", "description": "以JSON数组格式输出用户上传的图片列表", "label": "图片信息", "type": "source", "targets": [], "key": "images"},
                        {"valueType": "boolean", "description": "当未点击任何按钮时值为true", "label": "未点击按钮", "type": "source", "targets": [], "key": "unclickedButton"},
                        {"valueType": "boolean", "description": "运行完成后开关打开，下游链接组件开始运行。", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "questionInput",
                    "inputs": [
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游所有条件方可激活当前组件执行逻辑", "label": "联动激活", "type": "target", "keyType": "trigger", "value": False, "key": "switch"},
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游任一条件即可激活当前组件执行逻辑", "label": "任一激活", "type": "target", "keyType": "triggerAny", "value": False, "key": "switchAny"},
                        {"valueType": "boolean", "description": "输入文本开关", "label": "输入文本", "type": "switch", "value": True, "key": "inputText"},
                        {"valueType": "boolean", "description": "上传文档开关", "label": "上传文档", "type": "switch", "value": True, "key": "uploadFile"},
                        {"valueType": "boolean", "description": "上传图片开关", "label": "上传图片", "type": "switch", "value": False, "key": "uploadPicture"},
                        {"valueType": "boolean", "description": "文档审查开关", "label": "文档审查", "type": "switch", "value": False, "key": "fileUpload"},
                        {"valueType": "boolean", "description": "是否开启文档比对功能", "label": "是否文档对比", "type": "checkBox", "value": False, "key": "fileContrast"},
                        {"valueType": "any", "description": "上传的文件列表,如果开启了文档对比,每个分组只能上传一个文件", "label": "文档分组", "type": "table", "value": [], "key": "fileInfo"},
                        {"valueType": "boolean", "description": "是否作为初始全局input", "label": "是否作为初始全局input", "type": "hidden", "value": True, "key": "initialInput"}
                    ],
                    "intro": "用户输入入口,对话中用户的输入信息,与其他模块连接,一般作为起始模块",
                    "name": "用户提问",
                    "disabled": False,
                    "category": "用户提问"
                }
            },
            {
                "id": "pdf2md1",
                "type": "custom",
                "initialized": False,
                "position": {"x": 500, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "description": "识别结果", "label": "识别结果", "type": "source", "targets": [], "key": "pdf2mdResult"},
                        {"valueType": "boolean", "label": "执行成功", "type": "source", "targets": [], "key": "success"},
                        {"valueType": "boolean", "label": "执行异常", "type": "source", "targets": [], "key": "failed"},
                        {"valueType": "boolean", "description": "运行完成后开关打开，下游链接组件开始运行。", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "pdf2md",
                    "inputs": [
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游所有条件方可激活当前组件执行逻辑", "label": "联动激活", "type": "target", "keyType": "trigger", "value": False, "key": "switch"},
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游任一条件即可激活当前组件执行逻辑", "label": "任一激活", "type": "target", "keyType": "triggerAny", "value": False, "key": "switchAny"},
                        {"connected": True, "valueType": "file", "description": "", "label": "文档信息", "type": "target", "value": "", "key": "files"},
                        {"valueType": "selectPdf2mdModel", "description": "", "label": "选择模型", "type": "selectPdf2mdModel", "value": "deep_pdf2md", "key": "pdf2mdType", "required": True}
                    ],
                    "intro": "通用文档解析，将pdf/doc等转成markdown格式",
                    "name": "通用文档解析",
                    "disabled": False
                }
            },
            {
                "id": "confirmreply1",
                "type": "custom",
                "initialized": False,
                "position": {"x": 1000, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "description": "回复内容原样输出。", "label": "回复内容", "type": "source", "value": "", "key": "text"},
                        {"valueType": "boolean", "description": "运行完成后开关打开，下游链接组件开始运行。", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "confirmreply",
                    "inputs": [
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游所有条件方可激活当前组件执行逻辑", "label": "联动激活", "type": "target", "keyType": "trigger", "value": False, "key": "switch"},
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游任一条件即可激活当前组件执行逻辑", "label": "任一激活", "type": "target", "keyType": "triggerAny", "value": False, "key": "switchAny"},
                        {"connected": False, "valueType": "boolean", "description": "控制回复内容是否输出给用户", "label": "回复对用户可见", "type": "switch", "value": True, "key": "stream"},
                        {"connected": True, "valueType": "string", "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}", "label": "回复内容", "type": "textarea", "value": "文件内容：{{@pdf2md1_pdf2mdResult}}", "key": "text"}
                    ],
                    "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                    "name": "确定回复",
                    "disabled": False,
                    "category": "大模型"
                }
            },
            {
                "id": "ai1",
                "type": "custom",
                "initialized": False,
                "position": {"x": 1500, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "boolean", "description": "当模型运行结束，生成所有内容后，则回复结束下游组件开启。", "label": "回复结束", "type": "source", "targets": [], "key": "isResponseAnswerText"},
                        {"valueType": "string", "description": "大模型处理完的信息，将作为回复内容进行输出。引用变量：", "label": "回复内容", "type": "source", "targets": [], "key": "answerText"},
                        {"valueType": "boolean", "description": "运行完成后开关打开，下游链接组件开始运行。", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "aiChat",
                    "inputs": [
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游所有条件方可激活当前组件执行逻辑", "label": "联动激活", "type": "target", "keyType": "trigger", "value": False, "key": "switch"},
                        {"connected": True, "valueType": "boolean", "description": "同时满足上游任一条件即可激活当前组件执行逻辑", "label": "任一激活", "type": "target", "keyType": "triggerAny", "value": False, "key": "switchAny"},
                        {"connected": True, "valueType": "string", "description": "引用变量：{{text}}", "label": "信息输入", "type": "target", "value": "", "key": "text"},
                        {"connected": True, "valueType": "image", "description": "引用变量：{{images}}", "label": "图片输入", "type": "target", "value": "", "key": "images"},
                        {"connected": True, "valueType": "search", "description": "引用变量：{{knSearch}}", "label": "知识库搜索结果", "type": "target", "value": "", "key": "knSearch"},
                        {"connected": False, "valueType": "text", "description": "知识库高级配置", "label": "知识库高级配置", "type": "target", "value": "...", "key": "knConfig"},
                        {"connected": False, "min": 0, "max": 6, "valueType": "chatHistory", "description": "", "step": 1, "label": "聊天上下文", "type": "inputNumber", "value": 3, "key": "historyText"},
                        {"valueType": "string", "description": "", "label": "选择模型", "type": "selectChatModel", "value": "doubao-deepseek-v3", "key": "model", "required": True},
                        {"valueType": "string", "description": "模型引导词，可通过调整该提示，引导模型聊天方向，该内容会被固定在开头。", "label": "提示词 (Prompt)", "type": "textarea", "value": "\n<角色>\n你是一个文件解答助手，你可以根据文件内容，解答用户的问题\n</角色>\n\n<文件内容>\n{{@pdf2md1_pdf2mdResult}}\n</文件内容>\n\n<用户问题>\n{{@question1_userChatInput}}\n</用户问题>\n            ", "key": "quotePrompt"},
                        {"connected": False, "valueType": "boolean", "description": "控制回复内容是否输出给用户", "label": "回复对用户可见", "type": "switch", "value": True, "key": "stream"},
                        {"min": 0, "max": 1, "markList": {"0": "严谨", "1": "创意"}, "valueType": "number", "description": "控制回复创意性，如果想要和输入信息一致的答案，数值越小越好；如果想要模型发挥创意性，数值越大越好。", "step": 0.1, "label": "回复创意性", "type": "slider", "value": 0.1, "key": "temperature"},
                        {"min": 0, "max": 1, "markList": {"0": "逻辑", "1": "感性"}, "valueType": "number", "description": "控制输出的多样性,值越大输出包括更多单词选项；值越小，输出内容更集中在高概率单词上，即输出更确定但缺少多样性。一般【回复创意性】和【核采样TOP_P】只设置一个。", "step": 0.1, "label": "核采样TOP_P", "type": "slider", "value": 1, "key": "topP"},
                        {"min": 100, "max": 16000, "markList": {"5000": "5000", "16000": 16000}, "valueType": "number", "step": 50, "label": "回复字数上限", "type": "slider", "value": 5000, "key": "maxToken"}
                    ],
                    "intro": "AI 对话模型，根据信息输入和提示词（Prompt）加工生成所需信息，展示给用户，完成与用户互动。",
                    "name": "智能对话",
                    "disabled": False,
                    "category": "大模型"
                }
            },
            {
                "id": "addMemoryVariable1",
                "type": "custom",
                "initialized": False,
                "position": {"x": 0, "y": 1500},
                "data": {
                    "outputs": [],
                    "moduleType": "addMemoryVariable",
                    "inputs": [
                        {"connected": True, "valueType": "string", "description": "", "label": "question1_userChatInput", "type": "agentMemoryVar", "targets": [], "key": "question1_userChatInput"},
                        {"connected": True, "valueType": "string", "description": "", "label": "pdf2md1_pdf2mdResult", "type": "agentMemoryVar", "targets": [], "key": "pdf2md1_pdf2mdResult"},
                        {"connected": True, "valueType": "string", "description": "", "label": "ai1_answerText", "type": "agentMemoryVar", "targets": [], "key": "ai1_answerText"}
                    ],
                    "intro": "使用该组件将变量存为记忆变量后，可以在智能体的其他组件中引用",
                    "name": "添加记忆变量",
                    "disabled": False,
                    "category": "高阶能力"
                }
            }
        ],
        "edges": [
            {"id": "61b3e9df-0014-4452-a55b-22b4664c2b5a", "type": "custom", "source": "simpleInputId", "target": "pdf2md1", "sourceHandle": "finish", "targetHandle": "switchAny", "data": {}, "label": "", "sourceX": 324, "sourceY": 1064.984375, "targetY": 438.6953125, "targetX": 496, "animated": False},
            {"id": "f2b238e4-351e-4630-8ae1-115b426f73b9", "type": "custom", "source": "simpleInputId", "target": "pdf2md1", "sourceHandle": "files", "targetHandle": "files", "data": {}, "label": "", "sourceX": 324, "sourceY": 926.984375, "targetY": 496.4921875, "targetX": 496, "animated": False},
            {"id": "b501d209-4802-4ce7-af4d-86842e5ba04e", "type": "custom", "source": "simpleInputId", "target": "addMemoryVariable1", "sourceHandle": "userChatInput", "targetHandle": "question1_userChatInput", "data": {}, "label": "", "sourceX": 324, "sourceY": 880.984375, "targetY": 1584.8984375, "targetX": -4, "animated": False},
            {"id": "d0b1333f-7f9b-4a42-b47c-b9d33a850ca0", "type": "custom", "source": "pdf2md1", "target": "confirmreply1", "sourceHandle": "finish", "targetHandle": "switchAny", "data": {}, "label": "", "sourceX": 864, "sourceY": 803.1875, "targetY": 438.6953125, "targetX": 996, "animated": False},
            {"id": "74711c62-2c77-47f0-b986-1d18eb84609a", "type": "custom", "source": "pdf2md1", "target": "addMemoryVariable1", "sourceHandle": "pdf2mdResult", "targetHandle": "pdf2md1_pdf2mdResult", "data": {}, "label": "", "sourceX": 864, "sourceY": 665.1875, "targetY": 1660.6953125, "targetX": -4, "animated": False},
            {"id": "5789e76f-75f8-456c-a2df-99b4ba08a333", "type": "custom", "source": "confirmreply1", "target": "ai1", "sourceHandle": "finish", "targetHandle": "switchAny", "data": {}, "label": "", "sourceX": 1324, "sourceY": 829.1875, "targetY": 438.6953125, "targetX": 1496, "animated": False},
            {"id": "8812b5b0-6faf-458d-9550-26b27f72ca92", "type": "custom", "source": "ai1", "target": "addMemoryVariable1", "sourceHandle": "answerText", "targetHandle": "ai1_answerText", "data": {}, "label": "", "sourceX": 1824, "sourceY": 1637.5625, "targetY": 1736.4921875, "targetX": -4, "animated": False}
        ],
        "position": [372.3680880974696, -103.04498594189312],
        "zoom": 0.463331771321462,
        "viewport": {"x": 372.3680880974696, "y": -103.04498594189312, "zoom": 0.463331771321462}
    }

    # 生成SDK代码
    generated_code = FlowGraph.from_json_to_code(
        json_data,
        auth_key="7217394b7d3e4becab017447adeac239",
        auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 打印生成的代码
    print("生成的SDK代码：")
    print("=" * 50)
    print(generated_code)
    print("=" * 50)

    # 将生成的代码保存到文件
    with open("generated_workflow.py", "w", encoding="utf-8") as f:
        f.write(generated_code)
    
    print("\n代码已保存到 generated_workflow.py 文件中！")

if __name__ == "__main__":
    main()
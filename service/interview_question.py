import json
import os

import requests

from utils import pdf_utils


def interview_question(file, position, experience):
    """
    面试问题生成
    :param file:
    :param position:
    :param experience:
    :return:
    """

    # 个人访问令牌   ###需要修改为自己的令牌token
    personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
    # 工作流ID（workflow_id）
    workflow_id = os.getenv('WORKFLOW_ID_INTERVIEW_QUESTION')
    # 应用ID（app_id）
    app_id = os.getenv('APP_ID')

    # 简历由PDF转换为文本类型
    resume = pdf_utils.extract_text_from_pdf(file)

    # 构造请求头
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # 构造请求体
    payload = {
        "workflow_id": workflow_id,
        ### 注意：字典中的key要求与工作流中的入口参数保持一致
        "parameters": {"resume": resume, "position": position, "work_experience": experience},
        ### 需要修改为自己的工作流项目ID
        "app_id": app_id
    }

    # 发送POST请求
    response = requests.post(
        "https://api.coze.cn/v1/workflow/run",
        headers=headers,
        json=payload
    )

    if response.ok:
        output = json.loads(json.loads(response.text)['data'])['output']
        return output, resume

    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)


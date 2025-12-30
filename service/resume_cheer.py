import json
import os

import markdown
import requests

from utils.pdf_utils import extract_text_from_pdf

def resume_cheer(file):
    """
    AI鼓励师服务
    :param file:
    :return:
    """

    resume_content = extract_text_from_pdf(file)

    # 个人访问令牌   ###需要修改为自己的令牌token
    personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
    # 工作流ID（workflow_id）
    workflow_id = os.getenv('WORKFLOW_ID_RESUME_CHEER')
    # 应用ID（app_id）
    app_id = os.getenv('APP_ID')


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
        "parameters": {"resume": resume_content},
        "app_id": app_id
    }

    print(payload)

    # 发送POST请求
    response = requests.post(
        "https://api.coze.cn/v1/workflow/run",
        headers=headers,
        json=payload
    )

    if response.ok:
        print(response.text)
        return markdown.markdown(json.loads(json.loads(response.text)['data'])['output'], extensions=['extra'])

    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)
import os

import markdown

from utils.pdf_utils import extract_text_from_pdf
import requests
import json

def resume_analysis(position, file):

    resume_content = extract_text_from_pdf(file)

    # 个人访问令牌   ###需要修改为自己的令牌token
    personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
    # 工作流ID（workflow_id）
    workflow_id = os.getenv('WORKFLOW_ID_RESUME_ANALYSIS')
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
        ### 注意：字典中的key要求与工作流中的入口参数保持一致
        "parameters": {"resume": resume_content, "position": position},  # 将input_text传递给input参数
        ### 需要修改为自己的工作流项目ID
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

        res = response.text

        # 获取需要的数据
        data = json.loads(json.loads(res)['data'])
        output = data['output']
        score = int(data['score'])

        print('========', output)
        print('========', score)
        return markdown.markdown(output, extensions=['extra']), score

    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)



if __name__ == '__main__':
    pass
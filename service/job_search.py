import os

import requests
import json


def job_search(job_name, salary_min, work_experience, city, company_name, education):
    """
    搜索岗位
    :param job_name:
    :param salary_min:
    :param work_experience:
    :param city:
    :param company_name:
    :param education:
    :return:
    """



    # 个人访问令牌   ###需要修改为自己的令牌token
    personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
    # 工作流ID（workflow_id）
    workflow_id = os.getenv('WORKFLOW_ID_JOB_SEARCH')
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
        "parameters": {"jobName": job_name, 'salaryMin': salary_min, 'city': city, "education": education, "workExperience": work_experience, "companyName": company_name},  # 将input_text传递给input参数
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
        data = json.loads(json.loads(response.text)['data'])
        output = data['output']
        print('========', output)

        return output
    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)

if __name__ == '__main__':
    job_search("Python开发工程师", 5000, 2, '', '', 7)
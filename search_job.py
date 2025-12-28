import requests
import json

# 搜索岗位
def search_jobs(jobName, salaryMin, workExperience, city, companyName, education):
    # 个人访问令牌   ###需要修改为自己的令牌token
    personal_access_token = "pat_gRdV1uSPBNma9F5GbH2Is4hiHup9UpF6X1shQAV0xSf5VOJCX841oF8lBXy4QwMt"
    # 应用ID（workflow_id）   ###需要修改为自己的搜索职位的工作流ID
    workflow_id = "7588067410273337353"

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
        "parameters": {"jobName": jobName, 'salaryMin': salaryMin, 'city': city, "education": education, "workExperience": workExperience, "companyName": companyName},  # 将input_text传递给input参数
        ### 需要修改为自己的工作流项目ID
        "app_id": "7588035589828968463"
    }

    print(payload)

    # 发送POST请求
    response = requests.post(
        "https://api.coze.cn/v1/workflow/run",
        headers=headers,
        json=payload
    )

    if response.ok:
        print("请求成功，返回数据：")
        print(response.text)
        res = response.text

        #获取需要的数据
        data1 = json.loads(res)['data']
        print('========',data1)
        # output = json.loads(data1)['jobdata']
        output = json.loads(data1)['output']
        print('========', output)
        data = []

        for i in output:
            print('查看没一次输出',i)

            # data.append(i['jobdata'][0])
            data.append(i)

        print('++++++++++++++++',data)

        return data
    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)

if __name__ == '__main__':
    search_jobs("Python开发工程师", 5000, 2, '','',7)
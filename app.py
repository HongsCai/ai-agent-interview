import markdown
from flask import Flask, render_template, request
from service.job_search import job_search
from service.resume_analysis import resume_analysis

app = Flask(__name__)

# 主页
@app.route('/')
def begin():
    return render_template('search.html')

# 简历分析
@app.route('/resume/', methods=['POST', 'GET'])
def resume():
    if request.method == 'GET':
        return render_template('resume_analysis.html')
    print("简历分析")
    position = request.form.get('position')
    file = request.files['resume']
    print("参数:", position, file)
    output, score = resume(position, file)
    return render_template('resume_result.html', output=output, score=score)


# 面试
@app.route('/interview/', methods=['POST', 'GET'])
def interview():
    return render_template('interview.html')


# 职位查询
@app.route('/job/', methods=['POST', 'GET'])
def job():
    if request.method == 'GET':
        return render_template('search.html')

    print("职位查询")

    # 接收参数 (增加简单的容错处理)
    job_name = request.form.get('jobName')
    # 处理可能为空的数字字段
    def get_int(key, default=0):
        val = request.form.get(key)
        return int(val) if val and val.isdigit() else default
    salary_min = get_int('salaryMin', 0)
    work_experience = get_int('workExperience', 1)
    education = get_int('education', 1)
    city = request.form.get('city')
    company_name = request.form.get('companyName')

    print("参数:", job_name, salary_min, work_experience, city, company_name, education)

    # 获取数据
    result_data = job_search(job_name, salary_min, work_experience, city, company_name, education)

    return render_template("search_result.html", data=result_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
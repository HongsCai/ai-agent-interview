from flask import Flask, render_template, request

from service import resume_cheer
from service.interview_analysis import interview_analysis
from service.interview_question import interview_question
from service.job_search import job_search
from service.resume_analysis import resume_analysis

app = Flask(__name__)

# 主页
@app.route('/')
def begin():
    return render_template('search.html')

# 职位查询
@app.route('/job/', methods=['POST', 'GET'])
def job():
    if request.method == 'GET':
        return render_template('search.html')

    print("职位查询")

    # 接收参数 (增加简单的容错处理)
    job_name = request.form.get('jobName')
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

# 简历分析
@app.route('/resume/', methods=['POST', 'GET'])
def resume():
    if request.method == 'GET':
        return render_template('resume_analysis.html')

    print("简历分析")
    position = request.form.get('position')
    file = request.files['resume']
    print("参数:", position, file)
    output, score = resume_analysis(position, file)
    return render_template('resume_result.html', output=output, score=score)

# 面试配置
@app.route('/interview/', methods=['POST', 'GET'])
def interview():
    if request.method == 'GET':
        return render_template('interview.html')
    print("面试")
    position = request.form.get('position')
    experience = request.form.get('experience')
    file = request.files['resume']
    print("参数: ", position, experience, file)

    output, text = interview_question(file, position, experience)
    print(output, text)
    return render_template('interview_chat.html', output=output, text=text, position=position, experience=experience)

# 面试回答
@app.route('/interview/chat/', methods=['POST'])
def interview_chat():
    print("面试回答")
    position = request.form.get('position')
    experience = request.form.get('experience')
    resume_content = request.form.get('resume_content')
    history = request.form.get('history')
    answers = request.form.get('answers')
    print("参数: ", position, experience, resume_content, history, answers)
    output, score = interview_analysis(position, experience, resume_content, history, answers)
    return render_template('interview_result.html', output=output, score=score)

@app.route('/cheer/', methods=['GET', 'POST'])
def cheer():
    if request.method == 'GET':
        return render_template('cheer.html')

    print('AI鼓励师')
    file = request.files['resume']
    print("参数:", file)
    output = resume_cheer.resume_cheer(file)
    return render_template('cheer_result.html', output=output)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
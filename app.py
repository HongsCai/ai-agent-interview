import markdown
from flask import Flask, render_template, request, redirect, url_for
from search_job import search_jobs
from analyse import analyse_resume

app = Flask(__name__)

@app.route('/')
def begin():
    return render_template('search.html')

@app.route('/analyse/', methods=['POST', 'GET'])
def analyse():
    if request.method == 'GET':
        return render_template('analyse.html')

    position = request.form.get('position')
    file = request.files['resume']

    output, score = analyse_resume(position, file)

    output_html = markdown.markdown(output, extensions=['extra'])


    return render_template('analyse_result.html', output=output_html, score=score)


@app.route('/interview/', methods=['POST', 'GET'])
def interview():
    return render_template('interview.html')



@app.route('/get_job/', methods=['POST', 'GET'])
def get_job():
    if request.method == 'GET':
        return render_template('search.html')

    print("正在查询职位...")

    # 接收参数 (增加简单的容错处理)
    jobName = request.form.get('jobName')

    # 处理可能为空的数字字段
    def get_int(key, default=0):
        val = request.form.get(key)
        return int(val) if val and val.isdigit() else default

    salaryMin = get_int('salaryMin', 0)
    workExperience = get_int('workExperience', 1)
    education = get_int('education', 1)
    city = request.form.get('city')
    companyName = request.form.get('companyName')

    print("参数:", jobName, salaryMin, workExperience, city, companyName, education)

    # 获取数据
    result_data = search_jobs(jobName, salaryMin, workExperience, city, companyName, education)

    return render_template("search_result.html", data=result_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    username = request.form['username']
    fname = request.form['fname']
    lname = request.form['lname']

    # Execute the shell command to generate the report
    command = f"maigret {username} --html"
    subprocess.run(command, shell=True)

    # Execute the profiler script to generate profiler data
    command2 = f"python profiler.py --name {fname} --lastname {lname}"
    subprocess.run(command2, shell=True)

    # Read the report content
    report_path = f'reports/report_{username}_plain.html'
    try:
        with open(report_path, 'r') as f:
            report_content = f.read()
    except FileNotFoundError:
        report_content = ''

    # Read the profiler content
    profiler_path = f'Reports/{fname}_{lname}/{lname}_{fname}.json'
    try:
        with open(profiler_path, 'r') as f:
            profiler_content = f.read()
    except FileNotFoundError:
        profiler_content = ''

    return {'report_content': report_content, 'profiler_content': profiler_content}

if __name__ == '__main__':
    app.run(debug=True)

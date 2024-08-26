from flask import Flask,render_template,request,redirect,url_for,send_file
import fitz
import subprocess
import os
from werkzeug.utils import secure_filename 
from fileinput import filename 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def landing_page():
    return render_template("landing.html")
    
@app.route('/choice')
def choose():
    return render_template("index.html")

@app.route('/rateit')
def rate():
    return render_template("rate.html")

@app.route('/makeit',methods=["POST","GET"])
def pdf():
    if request.method == "POST":
        arr = []
        arr.append(request.form['name'])
        arr.append(request.form['Email'])
        arr.append(request.form['Mobile'])
        arr.append(request.form['Portfolio'])
        arr.append(request.form['Portfolio'])
        arr.append(request.form['Github'])
        arr.append(request.form['Github'])
        arr.append(request.form['College'])
        arr.append(request.form['loc1'])
        arr.append(request.form['branch'])
        arr.append(request.form['gpa'])
        arr.append(request.form['courseduration'])
        arr.append(request.form['keycourse'])
        arr.append(request.form['Languages'])
        arr.append(request.form['Frameworks'])
        arr.append(request.form['Tools'])
        arr.append(request.form['Platforms'])
        arr.append(request.form['Soft Skills'])
        arr.append(request.form['comp1'])
        arr.append(request.form['exloc1'])
        arr.append(request.form['role1'])
        arr.append(request.form['dur1'])
        arr.append(request.form['key11'])
        arr.append(request.form['desc11'])
        arr.append(request.form['key12'])
        arr.append(request.form['desc12'])
        arr.append(request.form['key13'])
        arr.append(request.form['desc13'])
        arr.append(request.form['comp2'])
        arr.append(request.form['exloc2'])
        arr.append(request.form['role2'])
        arr.append(request.form['dur2'])
        arr.append(request.form['key21'])
        arr.append(request.form['desc21'])
        arr.append(request.form['key22'])
        arr.append(request.form['desc22'])
        arr.append(request.form['key23'])
        arr.append(request.form['desc23'])
        arr.append(request.form['proj1'])
        arr.append(request.form['prodesc1'])
        arr.append(request.form['proj2'])
        arr.append(request.form['prodesc2'])
        arr.append(request.form['award1'])
        arr.append(request.form['award2'])
        arr.append(request.form['award3'])
        arr.append(request.form['voltitle1'])
        arr.append(request.form['volloc1'])
        arr.append(request.form['voldesc1'])
        arr.append(request.form['voldur1'])
        arr.append(request.form['voltitle2'])
        arr.append(request.form['volloc2'])
        arr.append(request.form['voldesc2'])
        arr.append(request.form['voldur2'])
        generate(arr)
        return render_template("success.html")
    else:
        return render_template("makepage.html")
    
def generate(arr):
    make_file(arr)
    subprocess.call(['pdflatex', '-output-directory=static/outputs/','templates/Resume.tex'], shell=False)
    return 'a'

def make_file(arr):
    f = open('templates/sample1.txt','r')
    fo = open('templates/Resume.tex','w')
    k = f.read()
    answers = arr
    check = False
    c = 0
    for i in k:
        if i == '^':
            if check == False:
                check = True
                fo.write(answers[c])
                c+=1
            else:
                check = False
        else:
            if check == True:
                continue
            else:
                fo.write(i)
    return 'a'

@app.route('/download')
def download_file():
    file_path = os.path.join('static/outputs/Resume.pdf')
    return send_file(file_path, as_attachment=True)

@app.route('/success', methods=['POST'])
@app.route('/success', methods=['POST'])
def success():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        job_title = request.form['job_title']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Read PDF and extract text
        pdf_text = read_pdf(filepath)

        # Return a response with the extracted text and job title
        return f'File uploaded successfully with job title: {job_title}<br>PDF Text: {pdf_text}'
    
    return 'File upload failed', 400

def read_pdf(filepath):
    """Read PDF file and extract text."""
    doc = fitz.open(filepath)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

@app.route('/model')
def idkbhai():
    return str('yay')



if __name__ == '__main__':
    app.run(debug=True)
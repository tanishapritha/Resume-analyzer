import os
import zipfile
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(_name_)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_multiple_resumes', methods=['POST'])
def upload_multiple_resumes():
    if 'resume_zip' not in request.files:
        return "No file part"
    
    file = request.files['resume_zip']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'])
        
        # Analyze resumes
        job_requirements = {
            "job_description": request.form.get('jobDescription'),
            "skills": request.form.get('skills'),
            "experience": request.form.get('experience')
        }
        analysis_results = analyze_resumes(app.config['UPLOAD_FOLDER'], job_requirements)
        
        return render_template('result.html', results=analysis_results)

def analyze_resumes(folder, job_requirements):
    results = []
    for filename in os.listdir(folder):
        if filename.endswith(".pdf") or filename.endswith(".docx"):
            resume_path = os.path.join(folder, filename)
            matching_percentage = calculate_matching_percentage(resume_path, job_requirements)
            results.append({
                'filename': filename,
                'matching_percentage': matching_percentage,
                'message': 'You are fit for the job!' if matching_percentage > 50 else 'You might want to improve your skills.'
            })
    
    grouped_results = group_resumes_by_percentage(results)
    return grouped_results

def calculate_matching_percentage(resume_path, job_requirements):
    # Placeholder function for matching percentage calculation
    # Implement actual resume parsing and matching logic here
    return 75  # Example percentage

def group_resumes_by_percentage(results):
    grouped = {
        'high': [],
        'medium': [],
        'low': []
    }
    for result in results:
        if result['matching_percentage'] >= 75:
            grouped['high'].append(result)
        elif 50 <= result['matching_percentage'] < 75:
            grouped['medium'].append(result)
        else:
            grouped['low'].append(result)
    
    return grouped

if _name_ == '_main_':
    app.run(debug=True)
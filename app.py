from flask import Flask, request, render_template
from resume_parser import parse_resume
from job_matcher import compute_similarity, find_gaps

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files["resume"]
    job_description = request.form["job_description"]

    resume_file.save("data/temp_resume.pdf")

    # Parse resume
    resume_data = parse_resume("data/temp_resume.pdf")

    # Calculate match score
    match_score = compute_similarity(" ".join(resume_data["skills"]), job_description)

    # Find missing skills
    job_skills = job_description.split(", ")
    missing_skills = find_gaps(resume_data["skills"], job_skills)

    return render_template("results.html", name=resume_data["name"], match_score=match_score, missing_skills=missing_skills)

if __name__ == "__main__":
    app.run(debug=True)

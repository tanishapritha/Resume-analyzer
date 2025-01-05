from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text, job_description):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity_score = util.cos_sim(resume_embedding, job_embedding).item()
    return round(similarity_score * 100, 2)

def find_gaps(resume_skills, job_skills):
    missing_skills = [skill for skill in job_skills if skill.lower() not in resume_skills]
    return missing_skills

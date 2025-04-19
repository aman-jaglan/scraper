import re

# Suppose we have a list of skills extracted from resume
resume_skills = {"Python", "Java", "SQL", "AWS", "Docker", "TensorFlow", ... }

def extract_skills_from_text(text):
    """Basic keyword extraction: return set of skills found in text."""
    found = set()
    text_lower = text.lower()
    for skill in resume_skills:
        # simple substring match (could be improved with word boundaries)
        if skill.lower() in text_lower:
            found.add(skill)
    return found

def is_match(job, resume_skills, threshold=0.5):
    """
    job: dict with at least 'title' or 'description' field.
    resume_skills: set of skills from resume.
    threshold: fraction of resume skills that should match (0.5 means 50%)
    """
    # Combine job title and description for matching
    text = job.get("description", "") + " " + job.get("title", "")
    job_skills = extract_skills_from_text(text)
    if not job_skills:
        return False
    match_fraction = len(job_skills) / len(resume_skills)
    return match_fraction >= threshold

def filter_jobs_by_skills(jobs, resume_skills, threshold=0.5):
    matched_jobs = []
    for job in jobs:
        if is_match(job, resume_skills, threshold):
            matched_jobs.append(job)
    return matched_jobs

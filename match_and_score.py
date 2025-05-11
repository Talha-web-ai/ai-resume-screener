import os
from extract_resume import extract_text_from_pdf
from extract_keywords import extract_keywords_from_jd

def score_resume(resume_text, jd_keywords):
    resume_keywords = extract_keywords_from_resume(resume_text) # type: ignore

    # Calculate match count based on the presence of keywords
    match_count = sum(1 for keyword in jd_keywords if keyword in resume_keywords)

    # Confidence score as a simple match count
    score = match_count / len(jd_keywords) if len(jd_keywords) > 0 else 0

    return score


def process_all_resumes(jd_text, resume_folder="resumes/"):
    jd_keywords = extract_keywords_from_jd(jd_text)
    results = []

    for filename in os.listdir(resume_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_folder, filename)
            resume_text = extract_text_from_pdf(path)
            score = score_resume(resume_text, jd_keywords)
            results.append((filename, score))

    # Sort by score descending
    ranked = sorted(results, key=lambda x: x[1], reverse=True)

    print("\n📊 Resume Match Results:")
    for name, score in ranked:
        print(f"{name}: {score} keyword matches")

    return ranked

# Example usage
if __name__ == "__main__":
    job_description = """
    We are hiring a Python Developer with experience in Python, Django, APIs, and SQL.
    Familiarity with Git, Linux, and RESTful services is a bonus.
    """
    process_all_resumes(job_description)

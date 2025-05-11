def score_resume(resume_keywords: list, jd_keywords: list) -> float:
    """
    Scores a resume by calculating keyword overlap between resume and job description.

    Args:
        resume_keywords (list): Keywords extracted from the resume.
        jd_keywords (list): Keywords extracted from the job description.

    Returns:
        float: Similarity score as a percentage (0–100).
    """
    if not jd_keywords or not resume_keywords:
        return 0.0

    # Convert to lowercase sets for matching
    resume_set = set([kw.lower() for kw in resume_keywords])
    jd_set = set([kw.lower() for kw in jd_keywords])

    # Calculate intersection
    common_keywords = resume_set.intersection(jd_set)
    score = len(common_keywords) / max(len(jd_set), 1)

    return round(score * 10, 2)

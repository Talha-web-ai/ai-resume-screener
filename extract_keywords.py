# extract_keywords.py

import spacy # type: ignore

# Load English language model
nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_jd(jd_text: str) -> list:
    """
    Extracts meaningful keywords from a job description using POS tagging.

    Args:
        jd_text (str): Job description as a string.

    Returns:
        list: List of relevant keywords (nouns, proper nouns, adjectives).
    """
    doc = nlp(jd_text)
    keywords = [token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop]
    return list(set(keywords))  # Remove duplicates

def extract_keywords_from_resume(resume_text: str) -> list:
    """
    Extracts relevant keywords from a resume text.

    Args:
        resume_text (str): Resume content as plain text.

    Returns:
        list: List of keywords from the resume.
    """
    doc = nlp(resume_text)
    keywords = [token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop]
    return list(set(keywords))  # Remove duplicates





 #We are looking for a Data Analyst with experience in SQL, Python, Excel, and Power BI.
   # Responsibilities include data cleaning, dashboard creation, and insights presentation.
    #Knowledge of statistics and communication skills are a plus.
    
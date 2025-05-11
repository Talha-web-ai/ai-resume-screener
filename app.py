import streamlit as st # type: ignore
from extract_resume import extract_text_from_pdf
from extract_keywords import extract_keywords_from_jd, extract_keywords_from_resume
from score import score_resume
import pandas as pd # type: ignore
import base64
import altair as alt # type: ignore

# -------------------- UI Header -------------------- #
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🧠 AI Resume Screener")
st.markdown("Upload a job description and multiple resumes to find the best match.")

# -------------------- Input Section -------------------- #
job_desc_input = st.text_area("📄 Job Descriptions (Paste text for each job in new line)", height=200)

uploaded_files = st.file_uploader(
    "📁 Upload Resumes (PDFs)",
    accept_multiple_files=True,
    type=["pdf"]
)

# Initialize session state if not exists
if "results_df" not in st.session_state:
    st.session_state.results_df = None
    st.session_state.resume_cache = None
    st.session_state.jd_keywords = None

# -------------------- Analyze Button -------------------- #
if st.button("🔍 Analyze Resumes"):
    if job_desc_input and uploaded_files:
        jd_keywords = extract_keywords_from_jd(job_desc_input.strip())
        results = []
        resume_cache = {}

        for resume_file in uploaded_files:
            resume_bytes = resume_file.read()
            if resume_bytes:
                resume_cache[resume_file.name] = resume_bytes
                resume_text = extract_text_from_pdf(resume_bytes)
                resume_keywords = extract_keywords_from_resume(resume_text)

                matched_keywords = set([kw.lower() for kw in resume_keywords]) & set([kw.lower() for kw in jd_keywords])
                score = score_resume(resume_keywords, jd_keywords)

                results.append({
                    'Resume': resume_file.name,
                    'Score (%)': score,
                    'Matched Keywords': ', '.join(matched_keywords)
                })

        results_df = pd.DataFrame(results)

        def get_fit_tag(score):
            if score >= 8.0:
                return "✅ Excellent Fit"
            elif score >= 5.0:
                return "⚠️ Potential Fit"
            else:
                return "❌ Not a Fit"

        results_df["Job Fit"] = results_df["Score (%)"].apply(get_fit_tag)

        # Save to session state
        st.session_state.results_df = results_df
        st.session_state.resume_cache = resume_cache
        st.session_state.jd_keywords = jd_keywords

        st.success("✅ Analysis Complete!")

    else:
        st.error("🚫 Please provide both job descriptions and resumes for analysis.")

# -------------------- Display Results if Available -------------------- #
if st.session_state.results_df is not None:
    results_df = st.session_state.results_df
    resume_cache = st.session_state.resume_cache
    jd_keywords = st.session_state.jd_keywords

    st.write("### 🔧 Filter and Sort Results")
    min_score = st.slider("Minimum Score", 0.0, 10.0, 0.0, 0.5)
    sort_option = st.selectbox("Sort By", ["Score (High to Low)", "Score (Low to High)", "Resume Name (A-Z)"])

    filtered_df = results_df[results_df["Score (%)"] >= min_score]

    if sort_option == "Score (Low to High)":
        filtered_df = filtered_df.sort_values(by="Score (%)", ascending=True)
    elif sort_option == "Resume Name (A-Z)":
        filtered_df = filtered_df.sort_values(by="Resume")
    else:
        filtered_df = filtered_df.sort_values(by="Score (%)", ascending=False)

    st.write("### 📊 Resume Match Scores with Job Fit Tags:")
    st.dataframe(filtered_df, use_container_width=True)

    # -------------------- Bar Chart -------------------- #
    st.write("### 📈 Resume Scores Bar Chart (0–10 Scale)")
    bar_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('Resume:N', sort='-y', title='Resume'),
        y=alt.Y('Score (%):Q', scale=alt.Scale(domain=[0, 10]), title='Score (0–10)'),
        color=alt.Color('Job Fit:N', legend=None)
    ).properties(width=700, height=400)

    st.altair_chart(bar_chart, use_container_width=True)

    # -------------------- Smart Suggestions -------------------- #
    st.write("### 💡 Smart Suggestions for Improvement")

    suggestions = []
    for index, row in filtered_df.iterrows():
        resume_name = row['Resume']
        resume_text = extract_text_from_pdf(resume_cache[resume_name])
        resume_keywords = extract_keywords_from_resume(resume_text)

        jd_kw_set = set(kw.lower() for kw in jd_keywords)
        resume_kw_set = set(kw.lower() for kw in resume_keywords)
        missing_keywords = jd_kw_set - resume_kw_set

        top_missing = list(missing_keywords)[:5]
        suggestion_text = ", ".join(top_missing) if top_missing else "✅ No major missing keywords."
        suggestions.append({'Resume': resume_name, 'Suggestions': suggestion_text})

    suggestions_df = pd.DataFrame(suggestions)
    st.dataframe(suggestions_df, use_container_width=True)

    # -------------------- CSV Download -------------------- #
    def get_table_download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="resume_scores.csv">📥 Download Results as CSV</a>'

    st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

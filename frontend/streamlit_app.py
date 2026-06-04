import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide",
)

st.title("AI Resume Screener")
st.write(
    "Upload a resume PDF and paste a job description to generate a structured hiring-fit analysis."
)

resume_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"],
)

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the full job description here...",
)

if st.button("Analyze Resume"):
    if resume_file is None:
        st.error("Please upload a resume PDF.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        files = {
            "resume_file": (
                resume_file.name,
                resume_file.getvalue(),
                "application/pdf",
            )
        }

        data = {
            "job_description": job_description,
        }

        try:
            response = requests.post(
                f"{API_URL}/analyze-resume",
                files=files,
                data=data,
                timeout=90,
            )

            if response.status_code == 200:
                result = response.json()

                st.success("Analysis completed successfully.")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Candidate", result["candidate_name"])

                with col2:
                    st.metric("Target Role", result["target_role"])

                with col3:
                    st.metric("Match Score", f'{result["match_score"]}/100')

                st.subheader("Matched Skills")
                st.write(result["matched_skills"])

                st.subheader("Missing Skills")
                st.write(result["missing_skills"])

                st.subheader("Experience Fit")
                st.write(result["experience_fit"])

                st.subheader("Education Fit")
                st.write(result["education_fit"])

                st.subheader("Risk Flags")
                for flag in result["risk_flags"]:
                    st.warning(flag)

                st.subheader("Recommended Improvements")
                for improvement in result["recommended_improvements"]:
                    st.write(f"- {improvement}")

                st.subheader("Interview Questions")
                for question in result["interview_questions"]:
                    st.write(f"- {question}")

                with st.expander("Extracted Resume Preview"):
                    st.write(result["extracted_resume_preview"])

                with st.expander("Raw JSON Response"):
                    st.json(result)

            else:
                st.error("API request failed.")
                st.json(response.json())

        except requests.exceptions.RequestException as error:
            st.error(f"Could not connect to the API: {error}")
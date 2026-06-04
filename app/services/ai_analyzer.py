from openai import OpenAI

from app.config import settings
from app.schemas import AIResumeAnalysis


def analyze_resume_with_ai(
    resume_text: str,
    job_description: str,
) -> AIResumeAnalysis:
    """
    Analyze a resume against a job description using OpenAI Structured Outputs.
    """

    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.openai_api_key)

    trimmed_resume_text = resume_text[:3000]
    trimmed_job_description = job_description[:2500]

    response = client.responses.parse(
        model=settings.openai_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter and AI hiring analyst. "
                    "Analyze the candidate resume against the job description. "
                    "Return only structured data that follows the schema. "
                    "Do not invent candidate experience. If evidence is missing, mark it as missing or weak."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Resume text:\n"
                    f"{trimmed_resume_text}\n\n"
                    "Job description:\n"
                    f"{trimmed_job_description}"
                ),
            },
        ],
        text_format=AIResumeAnalysis,
    )

    return response.output_parsed
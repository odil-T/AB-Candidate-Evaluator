import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


class ResumeJD(BaseModel):
    resume_text: str
    job_desc_text: str

class Transcript(BaseModel):
    text: str


@app.post("/resumes")
def evaluate_resume(resume_jd: ResumeJD):
    prompt = f"""Your task is to evaluate a candidate by comparing their resume with the job description. Pay attention to the candidate's relevant skills, experience, education, certifications, and projects. Also, lookout for gaps or inconsistencies in employment as well as frequent job hops.
    Follow a structured evaluation process:
    1. First, identify the candidate's key strengths — what makes them a strong match for the role.
    2. Then, identify the weaknesses or risks — what may make them less suited or raise concerns.
    3. Only after this reflection, provide an overall evaluation in this format:

    Final Score: A score from 1 to 10.

    ####
    Here is the job description:
    {resume_jd.job_desc_text}
    ####

    ####
    Here is the candidate's resume:
    {resume_jd.resume_text}
    ####
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert talent evaluator and hiring assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.15,
        stream=False
    )

    return {"response": response.choices[0].message.content}


@app.post("/transcripts")
def evaluate_transcript(transcript: Transcript):
    prompt = f"""Ваша задача оценить кандидата, проанализировав расшифровку его интервью. Обратите внимание на настроение и тон кандидата, качество и содержание его ответов, логичность аргументации, коммуникативные навыки и наличие критического мышления. Покажите своё рассуждение пошагово перед выставлением оценок. Вам нужно будет оценить кандидата по следующим критериям: профессионализм, качество ответов и коммуникативные навыки по шкале от 1 до 10. После этого выставьте итоговую оценку по шкале от 1 до 10. Структурируйте свой ответ в следующем формате:

    Рассуждение:
    
    Оценка профессионализма:
    Оценка качества ответов:
    Оценка коммуникативных навыков:
    Итоговая оценка:

    ####
    Вот расшифровка интервью:
    {transcript.text}
    ####
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Вы эксперт по оценке талантов и помощник по найму."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.15,
        stream=False
    )

    return {"response": response.choices[0].message.content}


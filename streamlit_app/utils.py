import os
import re
import PyPDF2
import streamlit as st

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RESUMES_DIR = "../candidates/resumes"
TRANSCRIPTS_DIR = "../candidates/transcripts"


@st.cache_data
def extract_jd_resumes():
    with open("../candidates/job-description.txt", "r") as file:
        job_description = file.read()

    resumes = []
    for resume_filename in os.listdir(RESUMES_DIR):
        with open(os.path.join(RESUMES_DIR, resume_filename), "rb") as file:
            reader = PyPDF2.PdfReader(file)
            resume = ""
            for page in reader.pages:
                resume += page.extract_text()
            resumes.append(resume)

    return job_description, resumes


@st.cache_data
def evaluate_from_resume(job_description: str, resume: str):
    prompt = f"""Your task is to evaluate a candidate by comparing their resume with the job description. Pay attention to the candidate's relevant skills, experience, education, certifications, and projects. Also, lookout for gaps or inconsistencies in employment as well as frequent job hops.
    Follow a structured evaluation process:
    1. First, identify the candidate's key strengths — what makes them a strong match for the role.
    2. Then, identify the weaknesses or risks — what may make them less suited or raise concerns.
    3. Only after this reflection, provide an overall evaluation in this format:

    Final Score: A score from 1 to 10.
    Candidate's Name: Their first name.

    ####
    Here is the job description:
    {job_description}
    ####

    ####
    Here is the candidate's resume:
    {resume}
    ####
    """

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
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
        temperature=0.2,
        max_completion_tokens=8192,
        top_p=0.8,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    pattern1 = r"Final Score: (\d+)"
    pattern2 = r"Candidate's Name: ([A-Za-z]+)"
    match1 = re.search(pattern1, response)
    match2 = re.search(pattern2, response)

    score = match1.group(1)
    name = match2.group(1)

    return name, score, response


@st.cache_data
def extract_transcripts():
    position = "Middle Data Analyst"
    transcripts = []
    for transcript_filename in os.listdir(TRANSCRIPTS_DIR):
        with open(os.path.join(TRANSCRIPTS_DIR, transcript_filename), "rb") as file:
            transcript = file.read()
            transcripts.append(transcript)
    return position, transcripts


@st.cache_data
def evaluate_from_transcript(position: str, transcript: str):
    prompt = f"""Your task is to evaluate a candidate for the {position} position by analyzing their interview transcript. Pay attention to the sentiment and tone of the candidate, the quality and content of their answers, the coherence of arguments, their communication skills, and evidence of critical thinking. Show your reasoning step by step before giving a final score to the candidate. Structure your response in this format:

    Reasoning:
    Final Score: A score from 1 to 10.
    Candidate's Name: Their first name.

    ####
    Here is the interview transcript:
    {transcript}
    ####
    """

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
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
        temperature=0.2,
        max_completion_tokens=8192,
        top_p=0.8,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    pattern1 = r"Final Score: (\d+)"
    pattern2 = r"Candidate's Name: ([A-Za-z]+)"
    match1 = re.search(pattern1, response)
    match2 = re.search(pattern2, response)

    score = match1.group(1)
    name = match2.group(1)

    return name, score, response
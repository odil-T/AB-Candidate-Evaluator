import requests
import PyPDF2


with open(r"../candidates/resumes/resume4.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    resume = ""
    for page in reader.pages:
        resume += page.extract_text()

with open("../candidates/job-description.txt", "r") as file:
    job_description = file.read()

with open("../candidates/transcripts/transcript1.txt", "r", encoding="utf-8") as file:
    transcript = file.read()




response1 = requests.post(
    "http://localhost:8000/resumes",
    headers={"Content-Type": "application/json"},
    json={
        "resume_text": resume,
        "job_desc_text": job_description
    }
)
print(response1.json()["response"])
print("===========================================================================", end="\n\n\n")


response2 = requests.post(
    "http://localhost:8000/transcripts",
    headers={"Content-Type": "application/json"},
    json={
        "text": transcript
    }
)
print(response2.json()["response"])
import os
import re
import PyPDF2
import streamlit as st

from dotenv import load_dotenv
from groq import Groq
from utils import (
    extract_jd_resumes,
    evaluate_from_resume,
    extract_transcripts,
    evaluate_from_transcript
)


if "resume_names" not in st.session_state:
    st.session_state.resume_names = []
if "resume_scores" not in st.session_state:
    st.session_state.resume_scores = []
if "resume_responses" not in st.session_state:
    st.session_state.resume_responses = []
if "transcript_names" not in st.session_state:
    st.session_state.transcript_names = []
if "transcript_scores" not in st.session_state:
    st.session_state.transcript_scores = []
if "transcript_responses" not in st.session_state:
    st.session_state.transcript_responses = []


st.header("Candidate Evaluator")
with st.sidebar:
    tab = st.radio(
        "Evaluation Type",
        ["Resume Evaluation", "Transcript Evaluation"]
    )

if tab == "Resume Evaluation":
    if st.button("Evaluate"):
        if not st.session_state.resume_names:
            job_description, resumes = extract_jd_resumes()

            for resume in resumes:
                name, score, response = evaluate_from_resume(job_description, resume)

                st.session_state.resume_names.append(name)
                st.session_state.resume_scores.append(score)
                st.session_state.resume_responses.append(response)


    with st.container():
        col1, col2, col3 = st.columns([1, 1, 4])
        col1.markdown("### Name")
        col2.markdown("### Score")
        col3.markdown("### Response")

        for n, s, r in zip(st.session_state.resume_names, st.session_state.resume_scores, st.session_state.resume_responses):
            col1, col2, col3 = st.columns([1, 1, 4])
            col1.write(n)
            col2.write(s)
            with col3:
                with st.expander("Show full response"):
                    st.write(r)
elif tab == "Transcript Evaluation":
    if st.button("Evaluate"):
        if not st.session_state.transcript_names:
            position, transcripts = extract_transcripts()

            for transcript in transcripts:
                name, score, response = evaluate_from_transcript(position, transcript)

                st.session_state.transcript_names.append(name)
                st.session_state.transcript_scores.append(score)
                st.session_state.transcript_responses.append(response)


    with st.container():
        col1, col2, col3 = st.columns([1, 1, 4])
        col1.markdown("### Name")
        col2.markdown("### Score")
        col3.markdown("### Response")

        for n, s, r in zip(st.session_state.transcript_names, st.session_state.transcript_scores, st.session_state.transcript_responses):
            col1, col2, col3 = st.columns([1, 1, 4])
            col1.write(n)
            col2.write(s)
            with col3:
                with st.expander("Show full response"):
                    st.write(r)
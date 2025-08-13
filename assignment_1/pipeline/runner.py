import os
import asyncio
from main import run_pipeline
from utils.file_io import save_uploaded_files


def process_pipeline(resume_files, jd_file):
    os.makedirs("input/test_resume", exist_ok=True)
    os.makedirs("input/test_jd", exist_ok=True)

    asyncio.run(save_uploaded_files(resume_files, jd_file))
    return asyncio.run(run_pipeline("input/test_resume", "input/test_jd"))

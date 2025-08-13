import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # store securely in .env
print(f"RAPIDAPI_KEY: {RAPIDAPI_KEY}")


def fetch_jobs(
    query: str, location: str = "India", page: int = 1, num_jobs: int = 5
):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }
    params = {
        "query": query,
        "location": location,
        "page": page,
        "num_pages": 1,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    jobs = response.json().get("data", [])[:num_jobs]
    return jobs

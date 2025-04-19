import requests, json
def get_jobs_on_greenhouse(board_url):
    jobs = []
    api_url = board_url.rstrip('/') + "?format=json"  # Greenhouse API endpoint for job board
    resp = requests.get(api_url)
    data = resp.json()
    for job in data.get("jobs", []):
        jobs.append({
            "title": job["title"],
            "company": data.get("company", ""),
            "location": job.get("location", ""),
            "link": job["absolute_url"],
            "source": "Greenhouse"
        })
    return jobs

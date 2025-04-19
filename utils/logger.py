import csv
from datetime import datetime

LOG_FILE = "applications_log.csv"

def log_application(job, status="applied"):
    # job is a dict with at least title, company, link, source
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Company", "Title", "Source", "Job Link", "Status"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            job.get("company", ""),
            job.get("title", ""),
            job.get("source", ""),
            job.get("link", ""),
            status
        ])

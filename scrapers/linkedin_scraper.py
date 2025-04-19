# scrapers/linkedin_scraper.py

import requests, time, random, csv
from bs4 import BeautifulSoup

# ─── Configuration ────────────────────────────────────────────────────────────

SEARCH_API = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
DETAIL_API = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}"

HEADERS = {
    "User-Agent":       "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept":           "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":  "en-US,en;q=0.9",
    "Referer":          "https://www.linkedin.com/jobs/",
    "X-Requested-With": "XMLHttpRequest",
}
JSON_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
}

# ─── Step 1: Fetch recent entry‑level job cards ────────────────────────────────

def fetch_recent_jobs(session, keywords, location, days=1, exp_level=2, pages=5, delay=(1,3)):
    """
    Returns list of dicts: {title, company, link, job_id}.
    """
    lookback = days * 86400
    jobs = []

    for pg in range(pages):
        params = {
            "keywords": keywords,
            "location": location,
            "f_TPR":    f"r{lookback}",
            "f_E":      str(exp_level),
            "start":    pg * 25,
        }
        resp = session.get(SEARCH_API, params=params)
        print(f"[Search {pg}] {resp.status_code}")
        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.job-search-card, div.base-search-card")
        if not cards:
            break

        for c in cards:
            # Title, company, link
            t = c.select_one("h3.base-search-card__title") or c.select_one("h3")
            comp = c.select_one("h4.base-search-card__subtitle") or c.select_one("h4")
            a = c.select_one("a.base-card__full-link") or c.find("a", href=True)
            title   = t.get_text(strip=True)    if t else ""
            company = comp.get_text(strip=True) if comp else ""
            link    = a["href"].split("?")[0]   if a and a.has_attr("href") else ""

            # Extract job_id from data-entity-urn="urn:li:jobPosting:4211834809"
            urn = c.get("data-entity-urn", "")
            job_id = urn.split(":")[-1] if urn else None

            if title and link and job_id:
                jobs.append({
                    "title":   title,
                    "company": company,
                    "link":    link,
                    "job_id":  job_id
                })
        time.sleep(random.uniform(*delay))

    return jobs

# ─── Step 2: Fetch full description via the JSON API ─────────────────────────

def fetch_description_via_api(session, job_id, delay=(1,3)):
    """
    Calls the guest jobPosting API and extracts the description HTML → text.
    """
    url = DETAIL_API.format(job_id)
    resp = session.get(url, headers=JSON_HEADERS)
    if resp.status_code != 200:
        print(f" → Detail API {job_id} returned {resp.status_code}")
        return ""
    try:
        data = resp.json()
    except ValueError:
        print(f" → Detail API {job_id} returned non-JSON")
        return ""

    # JSON can vary: check top‑level or under jobPosting
    html = data.get("description") \
        or data.get("jobPosting",{}).get("description") \
        or data.get("descriptionSnippet", "")
    if not html:
        return ""

    # strip HTML tags
    text = BeautifulSoup(html, "html.parser").get_text(separator="\n", strip=True)
    time.sleep(random.uniform(*delay))
    return text

# ─── Step 3: Fallback HTML parse (rarely needed) ─────────────────────────────

def fetch_description_requests(session, link, delay=(1,3)):
    """
    As a fallback, GET the job page and parse the #job-details or show-more HTML.
    """
    resp = session.get(link, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        return ""
    soup = BeautifulSoup(resp.text, "html.parser")
    desc = soup.find("div", id="job-details") \
        or soup.find("div", class_="show-more-less-html__markup") \
        or soup.find("div", class_="jobs-description__content")
    time.sleep(random.uniform(*delay))
    return desc.get_text(separator="\n", strip=True) if desc else ""

# ─── Step 4: Orchestrate & save to CSV ───────────────────────────────────────

def scrape_and_save(
    keywords="Data Analyst",
    location="United States",
    days=1,
    exp_level=2,
    pages=5,
    delay=(1,3),
    out_csv="linkedin_jobs_with_desc.csv"
):
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1) Job cards + IDs
    jobs = fetch_recent_jobs(session, keywords, location, days, exp_level, pages, delay)
    print(f"→ Found {len(jobs)} jobs (cards fetched).")

    # 2) Description via API
    enriched = []
    for job in jobs:
        desc = fetch_description_via_api(session, job["job_id"], delay)
        if not desc:
            desc = fetch_description_requests(session, job["link"], delay)
        enriched.append({
            "title":       job["title"],
            "company":     job["company"],
            "link":        job["link"],
            "description": desc
        })

    # 3) Write CSV
    if enriched:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=enriched[0].keys())
            writer.writeheader()
            writer.writerows(enriched)
        print(f"→ Saved {len(enriched)} jobs to {out_csv}")
    else:
        print("→ No jobs to save.")

if __name__ == "__main__":
    scrape_and_save()

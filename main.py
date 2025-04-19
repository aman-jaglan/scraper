# main.py

from scrapers.linkedin_scraper import fetch_recent_jobs_with_descriptions, save_to_csv

def main():
    # ─── Configuration ────────────────────────────────────────────────
    keywords         = "Data Analyst"      # job title to search
    location         = "United States"     # location filter
    days             = 1                   # past 24 hours
    experience_level = 2                   # Entry level
    pages            = 5                   # pages of 25 jobs each
    delay            = (1, 3)              # random pause (min,max seconds)

    # ─── Fetch & Enrich ───────────────────────────────────────────────
    enriched_jobs = fetch_recent_jobs_with_descriptions(
        keywords=keywords,
        location=location,
        days=days,
        experience_level=experience_level,
        max_pages=pages,
        delay=delay
    )
    print(f"Fetched {len(enriched_jobs)} entry‑level jobs (with descriptions).")

    # ─── Save Results ─────────────────────────────────────────────────
    save_to_csv(enriched_jobs, filename="linkedin_jobs_with_desc.csv")

if __name__ == "__main__":
    main()

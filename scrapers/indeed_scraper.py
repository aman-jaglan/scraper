import requests
from bs4 import BeautifulSoup

def get_jobs_on_indeed(query, location=None):
    jobs = []
    base_url = "https://www.indeed.com/jobs"
    params = {"q": query}
    if location:
        params["l"] = location
    page = 0
    while True:
        params["start"] = page * 10  # pagination parameter for indeed
        resp = requests.get(base_url, params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all('div', class_='job_seen_beacon')
        if not results:
            break
        for res in results:
            title_elem = res.find('h2')
            title = title_elem.text.strip() if title_elem else ""
            company_elem = res.find('span', class_='companyName')
            company = company_elem.text.strip() if company_elem else ""
            link_elem = res.find('a', attrs={'href': True})
            link = "https://indeed.com" + link_elem['href'] if link_elem else None
            jobs.append({"title": title, "company": company, "link": link, "source": "Indeed"})
        page += 1
    return jobs

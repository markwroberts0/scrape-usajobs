"""
example job listing:

    {
        'PositionID': 'JV-17-JEH-1938937',
        'ClockDisplay': '',
        'ShowMapIcon': True,
        'SalaryDisplay': 'Starting at $71,466 (VN 00)',
        'Title': 'Nurse Manager - Cardiology Service',
        'HiringPath': [{
            'IconClass': 'public',
            'Font': 'fa fa-users',
            'Tooltip': 'Jobs open to U.S. citizens, national or individuals who owe allegiance to the U.S.'
        }],
        'Agency': 'Veterans Affairs, Veterans Health Administration',
        'LocationLatitude': 33.7740173,
        'LocationLongitude': -84.29659,
        'WorkSchedule': 'Full Time',
        'Location': 'Decatur, Georgia',
        'Department': 'Department of Veterans Affairs',
        'WorkType': 'Agency Employees Only',
        'DocumentID': '467314300',
        'DateDisplay': 'Open 04/20/2017 to 05/16/2017'
    }
"""
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"
  }
)


import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS
import json
from time import sleep
from bs4 import BeautifulSoup

ak = os.getenv("AWS_ACCESS")
sak = os.getenv("AWS_SECRET")

BASE_URL = "https://www.usajobs.gov"
INTERVAL = 60 * 60 * 12

def save_job(job):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO jobs (
      title,
      department,
      location,
      agency,
      salary,
      url,
      low_grade,
      high_grade,
      job_grade,
      description,
      qualifications,
      requirements,
      search_id
    ) VALUES ( {title}, {department}, {location}, {agency}, {salary}, {url}, {low_grade}, {high_grade}, {job_grade}, {description}, {qualifications}, {requirements}, {search_id} )
    """.format(
        title = job["Title"],
        department = job["Department"],
        location = job["Location"],
        agency = job["Agency"],
        salary = job["SalaryDisplay"],
        url = job["PositionURI"],
        low_grade = job["LowGrade"],
        high_grade = job["HighGrade"],
        job_grade = job["JobGrade"],
        description = job["Description"],
        qualifications = job["Qualifications"],
        requirements = job["Requirements"],
        search_id = job["PositionID"]
    ))
    cursor.close()
    print("Job saved")

def scrape(session, query="",location="", page=1):
    print("scraping page: {}".format(page))
    url = "{base}/Search/?I={location}&k={query}&p={page}".format(
        base=BASE_URL, location=location, query=query, page=page
    )
    resp = session.get(url)
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    # fill search_id with hash value
    search_id = hash(html)

    cookies = dict(resp.cookies)
    headers = {
        "Origin": BASE_URL,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": url,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }
    data = {
        "GradeBucket": [],
        "JobCategoryCode": [],
        "LocationName": location,
        "PostingChannel": [],
        "Department": [],
        "Agency": [],
        "PositionOfferingTypeCode": [],
        "TravelPercentage": [],
        "PositionScheduleTypeCode": [],
        "SecurityClearanceRequired": [],
        "ShowAllFilters": [],
        "HiringPath": [],
        "Keyword": query,
        "Page": page,
        "UniqueSearchID": search_id,
    }

    resp = session.post(
        "{base}/Search/ExecuteSearch".format(base=BASE_URL),
        data=json.dumps(data),
    )
    if resp.status_code != 200:
        print("Error: status code {}".format(resp.status_code))
        print("Response: {}".format(resp.text))
        return
    payload = json.loads(resp.text)
    results = payload["Jobs"]

    for job in results:
        print("fetching details for: {}".format(job["Title"]))
        html = session.post(
            job["PositionURI"],
            cookies=cookies,
        )
        soup = BeautifulSoup(html.text, "html.parser")
        job["Description"] = soup.find("div", {"id": "duties"}).text
        job["Qualifications"] = soup.find("div", {"id": "qualifications"}).text
        job["Requirements"] = soup.find("div", {"id": "requirements"}).text
        save_job(job)

    if payload["Pager"]["CurrentPageIndex"] <= payload["Pager"]["LastPageIndex"]:
        next = payload["Pager"]["NextPageIndex"]
        fetched = False
        while not fetched:
            try:
                # with open("jobs.json", "a") as f:
                #     json.dump(results, f)
                scrape(query, page=next)
                fetched = True
            except session.exceptions.ConnectionError:
                sleep(5)
    return results


def on_job(job):
    """called on a new job listing, e.g. post to twitter or sth"""
    print("{} ({})".format(job["Title"], job["Location"]))


if __name__ == "__main__":
    try:
        jobs = json.load(open("jobs.json", "r"))
    except FileNotFoundError:
        jobs = {}

    with ApiGateway("https://www.google.com",
                regions=EXTRA_REGIONS,                                             
                access_key_id=f"{ak}",                                             
                access_key_secret=f"{sak}") as g:
        session = requests.Session()
        session.mount("hhttps://usajobs.gov", g)
        scrape(location="United States", session=session)

        print("done")
        exit()

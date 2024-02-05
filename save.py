import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS
import json
from time import sleep
from bs4 import BeautifulSoup

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
    ) VALUES ( `{title}`, `{department}`, `{location}`, `{agency}`, `{salary}`, `{url}`, `{low_grade}`, `{high_grade}`, `{job_grade}`, `{description}`, `{qualifications}`, `{requirements}`, `{search_id}` );
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

jobs = json.load(open("jobs.json", "r"))
for job in jobs:
    save_job(job)
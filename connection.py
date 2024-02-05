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

# read tables
cursor = connection.cursor()
print(cursor.execute("select * from jobs"))

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  department VARCHAR(255),
  location VARCHAR(255),
  agency VARCHAR(255),
  sub_agency VARCHAR(255),
  salary VARCHAR(255),
  url VARCHAR(255),
  low_grade INT,
  high_grade INT,
  job_grade VARCHAR(255),
  description TEXT,
  qualifications TEXT,
  requirements TEXT,
  search_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
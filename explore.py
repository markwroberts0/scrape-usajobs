# open jobs.json and count the number of jobs

import json

with open('jobs.json') as f:
    jobs = json.load(f)

print(len(jobs)) # 1000
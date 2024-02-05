import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS
from dotenv import load_dotenv
load_dotenv()
import os

ak = os.getenv("AWS_ACCESS")
sak = os.getenv("AWS_SECRET")

with ApiGateway("https://usajobs.gov",
                regions=EXTRA_REGIONS,
                access_key_id=f"{ak}",
                access_key_secret=f"{sak}") as g:
    session = requests.Session()
    session.mount("hhttps://usajobs.gov", g)

    response = session.get("https://usajobs.gov")
    print(response.status_code)

# from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS

# # Gateway to outbound HTTP IP and port for only two regions
# gateway_1 = ApiGateway("http://1.1.1.1:8080", regions=["eu-west-1", "eu-west-2"])

# # Gateway to HTTPS google for the extra regions pack, with specified access key pair
# gateway_2 = ApiGateway("https://www.google.com", regions=EXTRA_REGIONS, access_key_id="ID", access_key_secret="SECRET")

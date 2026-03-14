import os
import requests

env_dict = {}
with open('/home/sk/Downloads/Style DNA/.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env_dict[k] = v.strip('"\'')

APOLLO_API_KEY = env_dict.get("APOLLO_API_KEY")

url = "https://api.apollo.io/v1/mixed_people/search"
headers = {"Cache-Control": "no-cache", "Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}
data = {
    "q_organization_domains": "stripe.com",
    "person_titles": ["CTO"],
    "page": 1,
    "per_page": 2
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)

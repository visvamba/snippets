import requests

url = "https://www.google.com"

r = requests.get(url=url)

resp_obj = r.json()



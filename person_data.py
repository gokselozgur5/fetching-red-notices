import json
import requests
from urllib.parse import urlparse, parse_qs

api_url = "https://ws-public.interpol.int/notices/v1/red"
start_page = 1
result_per_page = 100
params={
    'resultPerPage': result_per_page,
    'page': start_page,
}
headers = {}
response = requests.request("GET", api_url, headers=headers, params=params)
if response.ok:
    data = response.json()
    total_page_url = data['_links']['last']['href']
    records = {}
    records[start_page]= data['_embedded']['notices']
    parsed_url = urlparse(total_page_url)
    query_params = parse_qs(parsed_url.query)
    total_page_number = int(query_params['page'][0])
    for i in range(start_page + 1, total_page_number + 1):
        response = requests.request("GET", api_url, headers=headers, params=params)
        records[i]= data['_embedded']['notices']
    with open('data.json', 'w') as f:
        json.dump(records, f)



    

    


    

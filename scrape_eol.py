import requests
from bs4 import BeautifulSoup
import yaml
import re

URL = "https://www.hardwarewartung.com/en/cisco-end-of-life-en/"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

data = []
table = soup.find('table')
if table:
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            model = cols[0].text.strip()
            eosl_date = cols[1].text.strip()
            data.append({'model': model, 'eosl_date': eosl_date})

if data:
    with open('cisco_eol.yaml', 'w') as yamlfile:
        yaml.dump(data, yamlfile, default_flow_style=False)
else:
    print("No data found")

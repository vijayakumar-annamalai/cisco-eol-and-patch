import requests
from bs4 import BeautifulSoup
import yaml
import re

BASE_URL = "https://www.parkplacetechnologies.com"
URL = "https://www.parkplacetechnologies.com/eosl/cisco/"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

family_links = []
# Find all the links to the family pages
for a in soup.find_all('a', href=re.compile(r'/eosl/family/')):
    family_links.append(a['href'])

all_data = []
for link in family_links:
    page_url = BASE_URL + link
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    table = page_soup.find('table')
    if table:
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                model = cols[0].text.strip()
                eosl_date = cols[1].text.strip()
                all_data.append({'model': model, 'eosl_date': eosl_date})

if all_data:
    with open('cisco_eol.yaml', 'w') as yamlfile:
        yaml.dump(all_data, yamlfile, default_flow_style=False)
else:
    print("No data found")

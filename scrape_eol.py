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
            # The date is in the second column. It can be in different formats.
            # Try to find a date in the format dd.mm.yyyy
            date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', cols[1].text.strip())
            if date_match:
                eosl_date = date_match.group(0)
            else:
                # If no date is found, check for the word "unknown"
                if "unknown" in cols[1].text.strip().lower():
                    eosl_date = "unknown"
                else:
                    # If neither a date nor "unknown" is found, we'll take the whole string
                    eosl_date = cols[1].text.strip()
            data.append({'model': model, 'eosl_date': eosl_date})

if data:
    with open('cisco_eol.yaml', 'w') as yamlfile:
        yaml.dump(data, yamlfile, default_flow_style=False)
else:
    print("No data found")

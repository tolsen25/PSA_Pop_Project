import requests
from bs4 import BeautifulSoup

import pandas as pd

# URL of the Wikipedia page with the table
url = 'https://www.psacard.com/pop/baseball-cards/20003'


r = requests.get(url)
bs = BeautifulSoup(r.text, "html.parser")

# Send an HTTP request to the URL
response = requests.get(url)

tableRows = bs.findAll('tr')

links = []
for row in tableRows[3:]: # start at the third tr
  firstTd = row.find("td")
  setUrl_text = firstTd.find("a")
  setUrl = setUrl_text.get('href')
  links.append(setUrl)
  print(setUrl_text)


df = pd.DataFrame(links)

df["links"] = "www.psacard.com"  + df[0]

df = df.iloc[:,1:]
df.to_csv("setLinks.csv", index = False)

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
  #print(setUrl_text)


df2 = pd.DataFrame(links)

df2["links"] = "https://www.psacard.com"  + df2[0]

df2 = df2.iloc[:,1:]
df2.to_csv("setLinks.csv", index = False)

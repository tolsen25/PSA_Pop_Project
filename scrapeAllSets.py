
import pandas as pd
import requests
from bs4 import BeautifulSoup

import time

urlTable = pd.read_csv("setLinks.csv")
pattern = r'/(\d{4}(?:-\d{2,4})?)/'

# Use str.extract to create a new 'Year' column
urlTable['Year'] = urlTable['links'].str.extract(pattern)


urls = urlTable["links"]

url = "https://www.psacard.com/pop/baseball-cards/2023/221547" # Test the connection
r = requests.get(url)

r.ok
len(r.text)

bs = BeautifulSoup(r.text, "html.parser")

# The first <tr> tag has the header information that we need
cardHeader = bs.find('tr', {'class' : 'text-uppercase'})

headers = []
for i in cardHeader.find_all('th'):
 title = i.text
 headers.append(title)
 
df = pd.DataFrame(columns = headers)
df = df.drop(df.columns[[0,2]], axis =1)
df.insert(1, "Year","")



sets=[]
testList=[]
#for rowNum, url in enumerate(urls):
for url in urls:
   # reset the list
  r = requests.get(url)
  if r.ok:
    bs = BeautifulSoup(r.text, "html.parser")
    time.sleep(3)
    cardRows = bs.find_all('tr') 
    Year = pd.Series(url).str.extract(pattern).iloc[0,0] # grabs the year from the url
    print(Year)
    #print("entering second for loop")
    for row in cardRows[2:]:
      testList = []
      set_TD = row.find("td", {"class": "text-left"})
      if set_TD:
        setName = set_TD.find("a").text
    
        sets.append(setName) # append set
        testList.append(setName)
        all_td = row.find_all("td")
     
        testList.append(Year) # append year
          #print(all_td)
        for td in all_td[3:]: 
          Grade = td.find("div").text
          testList.append(Grade) # append the grades
      
      newRow = pd.DataFrame([testList], columns = df.columns)
      df = pd.concat([df,newRow], ignore_index = True)
      else:
        print("Set name not found in row:", idx)
        #break
    print("Processed:", url)

df.to_pickle("allSets_final.pkl")


df[df["Year"] == "2019-20"]
df[df["Set Name"] == "Topps 582 Montgomery Set 2"]

df["Total"] = df["Total"].str.replace("", "")
df["Total"] = pd.to_numeric(df["Total"])
df["Total"].median()

df.to_pickle("last2years.pkl")
testPkl = pd.read_pickle("last2years.pkl")

from plotnine import ggplot, aes, geom_histogram,labs
plot = (ggplot(testPkl, aes(x='Total')) +
        geom_histogram(binwidth=5, fill='skyblue', color='black', alpha=0.7) +
        labs(
          
          title = "Title"
          
        ))


#df["Set Name"] = sets


# even_cardRows = bs.find_all('tr') 
# 
# sets=[]
# for idx, row in enumerate(even_cardRows[2:]):
#     set_TD = row.find("td", {"class": "text-left"})
#     setName = set_TD.find("a").text
#     sets.append(setName)
# 
#     all_td = row.find_all("td")
#     
#     # Assuming that you want to start extracting grades from the third column (index 2)
#     for i, td in enumerate(all_td[3:], start=3):
#         col = i - 2  # Column index in df
#         dfColumn = df.columns[col]
#         Grade = td.find("div").text
#         df.loc[idx, dfColumn] = Grade

df2= df.dropna()
df2.to_csv("allSets_withYear.csv")
df2.to_pickle("allSets_withYear.pkl")

myPickle = pd.read_pickle("allSets_withYear.pkl")

df["Set Name"] = sets        

df.to_csv("2023sets.csv")

# Tests -----------------------------------------------------------------------

for j,aRow in enumerate(urls[300:]):
  print(j)
  print(aRow)
  


for x in urls[290:]:
    year_match = pd.Series(x).str.extract(pattern).iloc[0,0]
    print(year_match)
    
  

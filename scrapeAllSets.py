import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

urlTable = pd.read_csv("setLinks.csv")
pattern = r'/(\d{4}(?:-\d{2,4})?)/'

# Use str.extract to create a new 'Year' column
urlTable['Year'] = urlTable['links'].str.extract(pattern)


urls = urlTable["links"]


url = "https://www.psacard.com/pop/baseball-cards/2023/221547"
r = requests.get(url)

r.ok
len(r.text)

bs = BeautifulSoup(r.text, "html.parser")




#cardTable = bs.find_all('table')

cardHeader = bs.find('tr', {'class' : 'text-uppercase'})

headers = []
for i in cardHeader.find_all('th'):
 title = i.text
 headers.append(title)
 
df = pd.DataFrame(columns = headers)
df = df.drop(df.columns[[0,2]], axis =1)
df.insert(1, "Year","")

numRows = 5000
df= pd.DataFrame(index=range(numRows), columns=df.columns) # I know how many sets there are so I can create and empty grid



# Concatenate the existing DataFrame with the DataFrame containing empty rows
#esult_df = pd.concat([existing_df, empty_rows_df], ignore_index=True)
sets=[]
#for rowNum, url in enumerate(urls):
for url in urls:
  r = requests.get(url)
  if r.ok:
    bs = BeautifulSoup(r.text, "html.parser")
    time.sleep(3)
    cardRows = bs.find_all('tr') 
    Year = pd.Series(url).str.extract(pattern).iloc[0,0] # grabs the year from the url
    print(Year)
    #print("entering second for loop")
    for idx, row in enumerate(cardRows[2:]):
      set_TD = row.find("td", {"class": "text-left"})
      if set_TD:
        setName = set_TD.find("a").text
        #print(setName)
        df.iloc[idx, 0] = setName # puts the set name in the first column
        sets.append(setName)
        all_td = row.find_all("td")
        df.iloc[idx,1] = Year # puts the year in the second column
      
          #print(all_td)
        for i, td in enumerate(all_td[3:], start=3): # Assuming that you want to start extracting grades from the third column (index 2)
          col = i - 1  # Starts putting the grades in the third column
          dfColumn = df.columns[col]
          Grade = td.find("div").text
          df.loc[idx, dfColumn] = Grade
      
      else:
        print("Set name not found in row:", idx)
        break
  
        
        #print(i)
 
    print("Processed:", url)


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
    
  

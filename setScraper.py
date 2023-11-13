import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.psacard.com/pop/baseball-cards/2023/221547"

r = requests.get(url)

r.ok

len(r.text)

bs = BeautifulSoup(r.text, "html.parser")

lenTags = len(bs.find_all('table'))


#cardTable = bs.find_all('table')

cardHeader = bs.find('tr', {'class' : 'text-uppercase'})
#cardTest = bs.find_all("th", {'class' : 'text-center sorting_disabled'})




# Obtain every title of columns with tag <th>
headers = []
for i in cardHeader.find_all('th'):
 title = i.text
 headers.append(title)
 
df = pd.DataFrame(columns = headers)
df = df.drop(df.columns[[0,2]], axis =1)

`# tr with the first set name inside the first a tag

# <tr> <td> <a> Set Name </a> </td> 
        #<td>
              #<div> Grade Number </div> 
              #<div> Plus numer </div>
              #<div> useless   </div>
              

even_cardRows = bs.find_all('tr') 
# td_elements = even_cardRows[6].find("td", {'class' : "text-left"})
# 
# x = even_cardRows[2].find_all("td")[3]
# x.find("div")
# 
# testTD = even_cardRows[2].find("td")
# 
# td_elements.find("a").text
#odd_cardRows = bs.find_all("tr", {'class' : 'even'})

for row in even_cardRows.find_all("td"):
  setName = row.find("a").text
  print(setName)

sets=[]

# for row in even_cardRows[2:]:
#     set_TD = row.find("td", {"class" : "text-left"})
#     setName = set_TD.find("a").text
#     sets.append(setName)
#     
#     all_td = row.find_all("td")
#     for td in all_td[2]:
#       Grade = td.find("div").text
#       print(Grade)
#   sets=[]
# for row in even_cardRows[2:]:
#     set_TD = row.find("td", {"class" : "text-left"})
#     setName = set_TD.find("a").text
#     sets.append(setName)
#     
#     all_td = row.find_all("td")
#     for i in range(3,len(all_td)):
#       for r in range(0,len(sets)):
#         col = i - 2 # i starts at 3 but we want to put the grade data starting with the second column
#         dfColumn = df.columns[col]
#         grade_td = all_td[i]  # Assuming you want to extract data from the third <td> in each row
#         Grade = grade_td.find("div").text
#         df.loc[r,dfColumn] = Grade
#         #print(Grade)
sets=[]
for idx, row in enumerate(even_cardRows[2:]):
    set_TD = row.find("td", {"class": "text-left"})
    setName = set_TD.find("a").text
    sets.append(setName)

    all_td = row.find_all("td")
    
    # Assuming that you want to start extracting grades from the third column (index 2)
    for i, td in enumerate(all_td[3:], start=3):
        col = i - 2  # Column index in df
        dfColumn = df.columns[col]
        Grade = td.find("div").text
        df.loc[idx, dfColumn] = Grade


df["Set Name"] = sets        

df.to_csv("2023sets.csv")

headers

daTags[0].text.strip() # strips out the white space # daTags is a list bruh

daNames = [item.text.strip() for item in daTags]

daTitle = bs.findAll('')

daTitle = bs.find_all(class_ = "PromoImageOnTopCircular-description promo-description")

titles = [daLooper.text.strip() for daLooper in daTitle]

daDataFrame =  pd.DataFrame(list(zip(titles, daNames)),columns = ["daTitle", "daName"])

daDataFrame.head


for i in range(3, len(all_td)):
  print(i)
  
  
  
  
  
  
  
  



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# What are some overall trends of PSA graded baseball cards?

myPickle = pd.read_pickle("allSets_final.pkl")
myPickle["Year"] = myPickle["Year"].str[:4]
myPickle = myPickle.drop("Total", axis = 1)
myPickle["Year"] = pd.to_datetime(myPickle['Year'], format = "%Y")

df_long = pd.melt(myPickle, id_vars=['Set Name', 'Year'], var_name='Grade', value_name='Count')
df_long["Count"] = df_long["Count"].str.replace("–","0")
df_long["Count"] = df_long["Count"].str.replace(",","")
df_long["Count"] =  pd.to_numeric(df_long["Count"])

df_long.to_pickle("tidySets.pkl")

myPickle.to_csv("allSets_wide.csv")

#df_long[df_long["Year"].dt.year > 1960].group_by("Year").count()

# Get the count of sets since 1960 ----------------------------------

result = myPickle[myPickle['Year'].dt.year > 1959].groupby(myPickle['Year'].dt.year).size().reset_index(name='Count')
result = result[result['Year'] < 2023]

#3plt.plot(result)

plt.plot(result['Year'], result['Count'], marker='o', linestyle='-', color='b')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Number of Different Sets')
plt.title('Count of Sets by Year (After 1960)')
plt.xticks(np.arange(result['Year'].min(), result['Year'].max(), 5))
plt.show()
plt.close()


# -----------------------------------------------------------------------------
from plotnine import *
from plotnine import percent_format
# What years had the highest total pop count?
# What sets had the highest gem rate?


lngSet = pd.read_pickle("tidySets.pkl")

#longSets2 = lngSet[lngSet["Year"].dt.year > 1959].groupby(lngSet["Year"].dt.year)


#lngSet %>% filter(Year > 1959) %>% groupby(Year) %>%  summarise(
  
 # Total_Pop = sum(Count)
 # Gems = sum( Grade == "Gem-MT10")
  
#)

result2 = (
    lngSet
    .loc[lngSet['Year'].dt.year > 1959]
    .groupby('Year')
    .agg(
        Total_Pop=('Count', 'sum'),
        Gems=('Count', lambda x: x[lngSet['Grade'] == 'GEM‑MT10'].sum())
    )
    .reset_index()
)


#result["Gem_MT_%"] = result["Gems"]/result["Count"] 
result2["Gem_MT_%"] = pd.to_numeric(result2["Gems"])/ pd.to_numeric(result2["Total_Pop"])

gem_mt = (ggplot(result2, mapping=aes(x="Year", y="Gem_MT_%"))
 + geom_area(color = "navy", fill = "cyan",alpha = .5) 
 + labs(title='Gem Percentage by Year Since 1960', x='Date', y='Gem Mint %')
 + scale_y_continuous(
    breaks=[0,.10,.20,.30,.40,.50,.60,.70,.80,.90]
     # scale=0.1 for displaying values as percentages
 ) 
 + theme_bw()
 
)

gem_mt.save("gem_mt.png", format="png", dpi=300)



#  ------------------------------------------------------

topSetPop = (
  lngSet
  .groupby(["Set Name", "Year"])
  .agg(
    Total_Pop = ("Count", "sum")
    
  )
  .reset_index()
  .sort_values(by="Total_Pop", ascending=False) 
  .head(50)
  
)

topSetPop["Year"] = topSetPop["Year"].dt.year
topSetPop["Set Name"] = topSetPop["Year"].astype(str) + " " + topSetPop["Set Name"]


topSetCol = (ggplot(topSetPop, mapping = aes(x = "Set Name", y = "Total_Pop")) +
            geom_col(fill = "lightblue", color = "blue", size = .5) +
            coord_flip() +
            scale_x_discrete(limits=topSetPop.sort_values('Total_Pop', ascending=True)['Set Name']) +
            theme_bw()+
            labs(
                title = "Total Number of Cards Graded for the Top 50 Sets",
                y = "Number of Cards Graded"
            )

)

topSetCol
topSetCol.save("topSetPopCol.png", format="png", dpi=300)

# -----------------------------------------------------------------------------------------------------------------------------------------

topSetPop2 = (
  lngSet
  .loc[lngSet['Year'].dt.year > 1999]
  .groupby(["Set Name", "Year"])
  .agg(
    Total_Pop = ("Count", "sum")
    
  )
  .reset_index()
  .sort_values(by="Total_Pop", ascending=False) 
  .head(10)
  
)

topSetPop2["Year"] = topSetPop2["Year"].dt.year
topSetPop2["Set Name"] = topSetPop2["Year"].astype(str) + " " + topSetPop2["Set Name"]

x = topSetPop2

recentCards = (ggplot(x, mapping = aes(x = "Set Name", y = "Total_Pop")) +
            geom_col(fill = "lightblue", color = "blue", size = .5) +
            coord_flip() +
            scale_x_discrete(limits=topSetPop2.sort_values('Total_Pop', ascending=True)['Set Name']) +
            theme_bw()+
            labs(
                title = "Total Number of Cards Graded for the Top 10 Sets since 2000",
                y = "Number of Cards Graded"
            )

)

recentCards




#----------------------------

x = lngSet[lngSet["Set Name"] == "Bowman"]


































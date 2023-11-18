
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

rs = df_long[df_long["Year"].dt.year > 1960]
import seaborn as sns
plt.bar("Set Name", "Count", hue = "Grade", data = rs)












View(myPickle)




test= pd.read_csv("allSets_withYear.csv")


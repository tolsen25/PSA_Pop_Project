
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from plotnine import *
import re

st.title("PSA Pop Report Dashboard")
st.subheader("Uncovering the trends of over 140 years of baseball card data")



@st.cache_data
def load_data():
    lngSet = pd.read_pickle("./pkl/tidySets.pkl")
    return lngSet

df = load_data()
df["Year"] = df["Year"].dt.year
df["Set Name"] = df["Year"].astype(str) + " " + df["Set Name"]
#lngSet = pd.read_pickle("tidySets.pkl")
#df = lngSet 

tab1, tab2, tab3 = st.tabs(["Scatter Plots", "Column Charts", "Line Plots"])
# --------------------------------------------------------------------------------------------
# Organizing types of charts with tabs
with tab1:
    # turning the grade into a number
    def extractGrade(s):
        match = re.search(r'(\d{1,2})\D*$', s)
        return int(match.group(1)) if match else 0


    df["Grade"] = df['Grade'].apply(lambda x: extractGrade(x))
    df["Grade"] = pd.to_numeric(df["Grade"])

    df["Year_Diff"] = 2023 - df["Year"]

    st.write("Choose the start year") # slider input
    min_year = st.slider('Year',1861,2022,1945)
    st.write("Each dot represents a set")
    st.write("Many years have lots of small sets, choose the minimum pop count")
    st.write("Note: The smaller the minimum the more datapoints and the longer it will take to load")
    min_size = st.slider('Minimum Number of Cards Graded',1,80000,1000)

    df2 = (
        df
        .loc[df['Year'] > min_year]
        .groupby(["Set Name", "Year", "Year_Diff"])
        .agg(
            Total_Pop=('Count', 'sum'),
            Gems=('Count', lambda x: x[df['Grade'] == 10].sum())
        )
        .reset_index()
    )


    df2["Gem_MT_%"] = df2["Gems"]/ df2["Total_Pop"]
    df2 = df2.loc[df2["Total_Pop"] > min_size]

    gemScatterPlot = (ggplot(df2,mapping = aes(x = "Year_Diff", y = "Gem_MT_%")) +
        geom_point() +
        labs(
            title = "Gem Mint% vs Years Ago from 2023",
            x = "Years Ago from 2023",
            y = "Gem Mint%",
            subtitle = "Min Pop " + str(min_size)
        ) +
        theme_bw()
        
        
        )

    st.pyplot(ggplot.draw(gemScatterPlot))
#--------------------------------------------------------------------------------------------------
with tab2:
    st.write("Choose the number of top sets for total cards") # slider input
    min_sets = st.slider('Number of Sets',3,25,15)

    st.write("Choose Year Range") # slider input
    min_age = st.slider('Year',1881,2022,(1999,2022))
    
    topSetPop = (
    df
    .loc[(df['Year'] > min_age[0]) & (df["Year"] < min_age[1])] 
    .groupby(["Set Name", "Year"])
    .agg(
        Total_Pop = ("Count", "sum")
        
    )
    .reset_index()
    .sort_values(by="Total_Pop", ascending=False) 
    .head(min_sets)
    
    )

    #topSetPop["Year"] = topSetPop["Year"].dt.year
    #topSetPop["Set Name"] = topSetPop["Year"].astype(str) + " " + topSetPop["Set Name"]


    topSetCol = (ggplot(topSetPop, mapping = aes(x = "Set Name", y = "Total_Pop")) +
                geom_col(fill = "lightblue", color = "blue", size = .5) +
                coord_flip() +
                scale_x_discrete(limits=topSetPop.sort_values('Total_Pop', ascending=True)['Set Name']) +
                theme_bw()+
                labs(
                    title = "Total Number of Cards Graded for the Top " +  str(min_sets) + " Sets",
                    subtitle = "From " + str(min_age[0]) + " to " + str(min_age[1]),
                    y = "Number of Cards Graded",
                    x = ""
                )

    )
    
    st.pyplot(ggplot.draw(topSetCol))
# -----------------------------------------------------------------------------------------------------------------
with tab3:
    st.write("More coming soon")
    myPickle = pd.read_pickle("./pkl/allSets_final.pkl")
    myPickle["Year"] = myPickle["Year"].str[:4]
    myPickle = myPickle.drop("Total", axis = 1)
    myPickle["Year"] = pd.to_datetime(myPickle['Year'], format = "%Y")

    result = myPickle[myPickle['Year'].dt.year > 1959].groupby(myPickle['Year'].dt.year).size().reset_index(name='Count')
    result = result[result['Year'] < 2023]

    linePlot = (ggplot(result, mapping = aes(x = "Year", y ="Count")) + 
            geom_line(color = "blue") +
            labs(
                title = "Number of Unique Sets since 1960"


            ) +
            theme_bw()
    
    )
    st.pyplot(ggplot.draw(linePlot))

    df3 = (
        df
        .groupby(["Set Name", "Grade","Year"])
        .agg(
            Total_Pop=('Count', 'sum')
        )
        .reset_index()
    )

    df3["avg"] = df3["Grade"] * df3["Total_Pop"]

    # Corrected aggregation
    df3 = (
        df3
        .groupby(["Set Name", "Year"])
        .agg(
            Mean=("avg", "sum"),
            Total_Pop=("Total_Pop", "sum")
        )
        .assign(Mean=lambda x: x["Mean"] / x["Total_Pop"])
        .reset_index()
    )

    

    x2 = (
        df3
        .groupby("Year")["Mean"]
        .mean()
        .reset_index()
    )
    
    linePlot = (ggplot(x2, mapping = aes(x = "Year", y = "Mean"))+
                geom_line() +
                labs(
                    y = "Average Grade",
                    title = "Average Grade Over Time"
                ) +
                theme_bw()
    )
    st.pyplot(ggplot.draw(linePlot))
    
    


    # year = st.slider('Year',1881,2022,1945)
    # df3 = (
    #     df2
    #     .loc[df2["Year"]== year]
    
    # )
    # df["Grade"] = df["Grade"].astype(str)
    # st.write(df3)
    
    # yearBoxes = (ggplot(df3,mapping = aes(x = "Set Name", y = "Gem_MT_%")) +
    #     geom_boxplot() 
        
        
        
    #     )
    # st.pyplot(ggplot.draw(yearBoxes))


#st.write(df2)











# df2 = (
#     df
#     .loc[df['Year'].dt.year > 1900]
#     .groupby(["Set Name", "Year", "Year_Diff"])
#     .agg(
#         Total_Pop=('Count', 'sum'),
#         Gems=('Count', lambda x: x[df['Grade'] == 10].sum())
#     )
#     .reset_index()
# )
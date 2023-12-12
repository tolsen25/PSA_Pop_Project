
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *
import re

st.title("PSA Pop Report Dashboard")
st.subheader("Uncovering the trends of over 140 years of baseball card data")



@st.cache_data
def load_data():
    lngSet = pd.read_pickle("tidySets.pkl")
    return lngSet

df = load_data()
df["Year"] = df["Year"].dt.year
df["Set Name"] = df["Year"].astype(str) + " " + df["Set Name"]
#lngSet = pd.read_pickle("tidySets.pkl")
#df = lngSet 

tab1, tab2, tab3 = st.tabs(["Scatter", "Col", "Box"])
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
    st.write("Many years have lots of small sets, choose the minimum pop count")
    st.write("Note: The smaller the minimum the more datapoints and the longer it will take to load")
    min_size = st.slider('Total_Pop',1,350000,1000)

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
    min_sets = st.slider('Num Sets',3,25,15)

    st.write("Choose the minimum year") # slider input
    min_age = st.slider('Year',1881,2022,1900)
    
    topSetPop = (
    df
    .loc[df['Year'] > min_age]
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
                    subtitle = "Since " + str(min_age),
                    y = "Number of Cards Graded",
                    x = ""
                )

    )

    st.pyplot(ggplot.draw(topSetCol))

st.write(df2)











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
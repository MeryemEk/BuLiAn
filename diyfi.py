###########################################################################################################
###########################################################################################################
###########################################################################################################
######## author = Meryem Elkalai
######## website = https://www.twitter.com//EkMeryem
######## layout inspired by  https://share.streamlit.io/tdenzl/bulian/main/BuLiAn.py
###########################################################################################################
###########################################################################################################
###########################################################################################################

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import seaborn as sns



#st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="expanded")


### Data Import ###

todate = pd.read_csv("data/todate_ASCSV.csv")
#todate['Date']=pd.to_datetime(todate['Date'])


### 
    
########################
### ANALYSIS METHODS ###
########################



#################
### SELECTION ###
#################



### Explanation ###
st.sidebar.markdown("**Give a name to your Food Index**")
FoodIndexName = st.sidebar.text_input('Your Index', placeholder='$TJX')
st.sidebar.markdown("**Select the region, ingredients and proportions of your index** 👇")
      



### REGION SELECTION ###
selected_region = st.sidebar.selectbox('Select the region where you want to see your Index',todate.Region.unique())
### PRODUCT SELECTION ###

selected_products=st.sidebar.multiselect("Select the products you want to have in your index. You can clear the current selection by clicking the corresponding x-button on the right", todate[todate['Region']==selected_region].Produit.unique(),default=['tomates','oranges','aubergines'])

###RECIPE INPUT BIS###
st.sidebar.markdown("For each ingredient, specify the quantity in g")
for i in range(len(selected_products)):
    ratios=st.sidebar.number_input(label=selected_products[i],step=100,key=i)
    
   
    
  


    


################
### ANALYSIS ###
################

    
    ## Extraire DataFrame avec les produits dans une liste
def extract_produits(df,produits):
    return df[df['Produit'].isin(produits)]

## Extraire DataFrame avec les régions dans une liste
def extract_regions(df,regions):
    return df[df['Region'].isin(regions)]

def your_index(region,PRODUITS,QTES):
    recette=pd.DataFrame({'Produit':PRODUITS , 'poids': QTES})
    recette['RATIO']=recette['poids']/recette.poids.sum()
    
    travail=pd.merge(extract_produits(todate[todate['Region']==region],PRODUITS),recette[['Produit','RATIO']],on='Produit')
    travail['Produit_index']=travail['Valeur']*travail['RATIO']
    travail=travail[['Date','Produit','Produit_index']]
    intermed=pd.pivot_table(travail,values='Produit_index',index='Date',columns='Produit',aggfunc=np.mean).reset_index().dropna()
    travail=travail[travail['Date'].isin(list(intermed.Date))]
    your_index=travail.groupby('Date').sum().reset_index()
    return your_index

    

    
resultat=your_index(selected_region,selected_products,ratios).sort_values(by='Date')
####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('DIY Food Index')
with row0_2:
    st.text("")
    st.subheader('by [Ek Meryem](https://twitter.com/EkMeryem)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello there! You can build your own Food Index and play with it.")
    st.markdown("Download your chart and publish it on Twitter with the #DIYFoodIndex")
    st.subheader('Here is the evolution of your index:')
    st.subheader(FoodIndexName)

    fig = plt.figure(figsize=(30, 16))
    sns.lineplot(x = "Date", y = "Produit_index", data = resultat,color = '#f21111')
    st.pyplot(fig)
    



  
    




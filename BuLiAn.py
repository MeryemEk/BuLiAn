###########################################################################################################
###########################################################################################################
###########################################################################################################
######## author = Tim Denzler
######## insitution = N/A
######## website = https://www.linkedin.com/in/tim-denzler/
######## version = 1.0
######## status = WIP
######## deployed at = https://share.streamlit.io/tdenzl/bulian/main/BuLiAn.py
######## layout inspired by https://share.streamlit.io/tylerjrichards/streamlit_goodreads_app/books.py
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


st.set_page_config(layout="wide")

### Data Import ###

todate = pd.read_csv("data/todate_ASCSV.csv")


### 
    
########################
### ANALYSIS METHODS ###
########################

def plot_x_per_season(attr,measure):
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### Goals
    attribute = label_attr_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute("season",attribute,measure)
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot, color = "#b80606")
    y_str = measure + " " + attr + " " + " per Team"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " by a Team"
        
    ax.set(xlabel = "Season", ylabel = y_str)
    if measure == "Mean" or attribute in ["distance","pass_ratio","possession","tackle_ratio"]:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 15),
                   textcoords = 'offset points')
    else:
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 15),
                   textcoords = 'offset points')
    st.pyplot(fig)

def plot_x_per_matchday(attr,measure):
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### Goals
    attribute = label_attr_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute("matchday",attribute,measure)
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), color = "#b80606")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)+1))
    y_str = measure + " " + attr + " per Team"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " by a Team"
        
    ax.set(xlabel = "Matchday", ylabel = y_str)
    if measure == "Mean" or attribute in ["distance","pass_ratio","possession","tackle_ratio"]:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    else:
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    st.pyplot(fig)

def plot_x_per_team(attr,measure): #total #against, #conceived
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### Goals
    attribute = label_attr_dict_teams[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute("team",attribute,measure)
    if specific_team_colors:
        ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), palette = color_dict)
    else:
        ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), color = "#b80606")
    y_str = measure + " " + attr + " " + "per Game"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + "in a Game"
    ax.set(xlabel = "Team", ylabel = y_str)
    plt.xticks(rotation=66,horizontalalignment="right")
    if measure == "Mean" or attribute in ["distance","pass_ratio","possession","tackle_ratio"]:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    else:
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    st.pyplot(fig)


    
def plt_attribute_correlation(aspect1, aspect2):
    df_plot = df_data_filtered
    rc = {'figure.figsize':(5,5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    asp1 = label_attr_dict_correlation[aspect1]
    asp2 = label_attr_dict_correlation[aspect2]
    if(corr_type=="Regression Plot (Recommended)"):
        ax = sns.regplot(x=asp1, y=asp2, x_jitter=.1, data=df_plot, color = '#f21111',scatter_kws={"color": "#f21111"},line_kws={"color": "#c2dbfc"})
    if(corr_type=="Standard Scatter Plot"):
        ax = sns.scatterplot(x=asp1, y=asp2, data=df_plot, color = '#f21111')
    #if(corr_type=="Violin Plot (High Computation)"):
    #    ax = sns.violinplot(x=asp1, y=asp2, data=df_plot, color = '#f21111')
    ax.set(xlabel = aspect1, ylabel = aspect2)
    st.pyplot(fig, ax)

def find_match_game_id(min_max,attribute,what):
    df_find = df_data_filtered
    search_attribute = label_fact_dict[attribute]
    if(what == "difference between teams"):
        search_attribute = "delta_" + label_fact_dict[attribute]
        df_find[search_attribute] = df_find[search_attribute].abs()
    if(what == "by both teams"):
        df_find = df_data_filtered.groupby(['game_id'], as_index=False).sum()
    column = df_find[search_attribute]
    index = 0
    if(min_max == "Minimum"):
        index = column.idxmin()
    if(min_max == "Maximum"):
        index = column.idxmax()
    #st.dataframe(data=df_find)
    game_id = df_find.at[index, 'game_id']
    value = df_find.at[index,search_attribute]
    team = ""
    if(what != "by both teams"):
        team = df_find.at[index, 'team']
    return_game_id_value_team = [game_id,value,team]
    return return_game_id_value_team

def build_matchfacts_return_string(return_game_id_value_team,min_max,attribute,what):
    game_id = return_game_id_value_team[0]
    df_match_result = df_data_filtered.loc[df_data_filtered['game_id'] == game_id]
    season = df_match_result.iloc[0]['season'].replace("-","/")
    matchday = str(df_match_result.iloc[0]['matchday'])
    home_team = df_match_result.iloc[0]['team']
    away_team = df_match_result.iloc[1]['team']
    goals_home = str(df_match_result.iloc[0]['goals'])
    goals_away = str(df_match_result.iloc[1]['goals'])
    goals_home = str(df_match_result.iloc[0]['goals'])    
    string1 =  "On matchday " + matchday + " of season " + season + " " + home_team + " played against " + away_team + ". "
    string2 = ""
    if(goals_home>goals_away):
        string2 = "The match resulted in a " + goals_home + ":" + goals_away + " (" + str(df_match_result.iloc[0]['ht_goals']) + ":" + str(df_match_result.iloc[1]['ht_goals']) +") win for " + home_team + "."
    if(goals_home<goals_away):
        string2 = "The match resulted in a " + goals_home + ":" + goals_away + " (" + str(df_match_result.iloc[0]['ht_goals']) + ":" + str(df_match_result.iloc[1]['ht_goals']) +") loss for " + home_team + "."
    if(goals_home==goals_away):
        string2 = "The match resulted in a " + goals_home + ":" + goals_away + " (" + str(df_match_result.iloc[0]['ht_goals']) + ":" + str(df_match_result.iloc[1]['ht_goals']) +") draw. "
    string3 = ""
    string4 = ""
    value = str(abs(round(return_game_id_value_team[1],2)))
    team = str(return_game_id_value_team[2])
    if(what == "difference between teams"):
        string3 = " Over the course of the match, a difference of " + value + " " + attribute + " was recorded between the teams."
        string4 = " This is the " + min_max.lower() + " difference for two teams in the currently selected data."
    if(what == "by both teams"):
        string3 = " Over the course of the match, both teams recorded " + value + " " + attribute + " together."
        string4 = " This is the " + min_max.lower() +" value for two teams in the currently selected data."
    if(what == "by a team"):
        string3 = " Over the course of the match, " + team + " recorded " + value + " " + attribute + "."
        string4 = " This is the " + min_max.lower() +" value for a team in the currently selected data."
    answer = string1 + string2 + string3 + string4
    st.markdown(answer)
    return df_match_result
    
####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('BuLiAn - Bundesliga Analyzer')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Tim Denzler](https://www.linkedin.com/in/tim-denzler/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello there! Have you ever spent your weekend watching the German Bundesliga and had your friends complain about how 'players definitely used to run more' ? However, you did not want to start an argument because you did not have any stats at hand? Well, this interactive application containing Bundesliga data from season 2013/2014 to season 2019/2020 allows you to discover just that! If you're on a mobile device, I would recommend switching over to landscape for viewing ease.")
    st.markdown("You can find the source code in the [BuLiAn GitHub Repository](https://github.com/tdenzl/BuLiAn)")
    st.markdown("If you are interested in how this app was developed check out my [Medium article](https://tim-denzler.medium.com/is-bayern-m%C3%BCnchen-the-laziest-team-in-the-german-bundesliga-770cfbd989c7)")
    
#################
### SELECTION ###
#################


st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')
### SEASON RANGE ###
st.sidebar.markdown("**Select the region, ingredients and proportions of your index** 👇")
      



### REGION SELECTION ###
selected_region = st.sidebar.selectbox('Select the region where you want to see your Index',todate.Region.unique())
### PRODUCT SELECTION ###

selected_products=st.sidebar.multiselect("Select the products you want to have in your index. You can clear the current selection by clicking the corresponding x-button on the right", todate.Produit.unique(), default = ['BLE DUR','TOMATES'])

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


### YOUR INDEX ###
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Evolution of your index')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown('Here is the evolution of your index')    

    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(x = "Date", y = "Produit_index", data = resultat,color = '#f21111')
    st.pyplot(fig)


  
    




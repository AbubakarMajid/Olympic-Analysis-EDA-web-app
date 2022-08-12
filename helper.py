import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
def medal_tally(df):

    medal_tally = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally =medal_tally.groupby('NOC')[['Gold', 'Silver', 'Bronze']].sum().sort_values(by='Gold', ascending=False)
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = df.region.dropna()
    country = country.unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def select_year_country(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df.region == country) & (medal_df.Year == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values(by='Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values(by='Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns = {'index':'Edition','Year':'Teams'},inplace = True)
    nations_over_time = nations_over_time.sort_values(by=['Edition'])
    return nations_over_time

def events_over_time(df):

    events = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index()
    events.rename(columns = {'index':'Years','Year':'Events'},inplace = True)
    events.sort_values(by = ['Years'], ascending = True,inplace = True)
    return events

def sports_events_over_years(df):
    return df.pivot_table(index = 'Sport', columns = 'Year',values = 'Event', aggfunc = 'nunique').fillna(0).astype(int)

def most_successfull_athletes(df,sport):
    df = df.dropna(subset = 'Medal')
    if sport != 'Overall':
        temp_df = df[df.Sport == sport]
        temp_df = temp_df.groupby(['Name','Sport','region'])['Medal'].count().reset_index().sort_values(by = ['Medal'], ascending = False).head(10)
        return temp_df
    else:
        temp_df = df.groupby(['Name','Sport','region'])['Medal'].count().reset_index().sort_values(by = ['Medal'], ascending = False).head(10)
        return temp_df


def country_wise_tally(df, country):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df.region == country]
    return temp_df.groupby('Year')['Medal'].count().reset_index()

def sports_events_over_years(df):
    return df.pivot_table(index = 'Sport', columns = 'Year',values = 'Event', aggfunc = 'nunique').fillna(0).astype(int)

def country_sports_medals(df,country):
    temp_df = df.dropna(subset = 'Medal')
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    temp_df = temp_df[temp_df.region == country].pivot_table(index = 'Sport', columns = 'Year', values = 'Medal',aggfunc = 'count').fillna(0).astype('int')
    return px.imshow(temp_df,text_auto = True,width = 800, height=800)

def most_successfull_athletes_country_wise(df,country):
    df = df.dropna(subset = 'Medal')
    temp_df = df[df.region == country]
    temp_df = temp_df.groupby(['Name','Sport','region'])['Medal'].count().reset_index().sort_values(by = ['Medal'], ascending = False).head(10)
    return temp_df

def weight_over_height_comparison(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df["Medal"].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df.Sport == 'Hockey']
        return temp_df
    else:
        return athlete_df

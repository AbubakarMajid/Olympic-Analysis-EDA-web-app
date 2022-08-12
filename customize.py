import pandas as pd

df1 = pd.read_csv('E:\\data_analytics_projects\\athlete_events.csv')
df2 = pd.read_csv('E:\\data_analytics_projects\\noc_regions.csv')

def preprocess():
    global df1, df2

    df1 = df1[df1['Season'] == 'Summer']
    df = df1.merge(df2, on = 'NOC',how = 'left')
    df.drop_duplicates(inplace =True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis = 1)
    return df
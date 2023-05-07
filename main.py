import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st
import customize
import helper
import scipy

df = customize.preprocess()
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio('Select an option',
                 ('Medal Tally','Athlete wise Analysis',
                  'Country wise analysis','Overall Analysis'))
#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.select_year_country(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in ' + str(selected_year) + 'Olypics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally for ' + str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f'Medal tally for {selected_country} in {selected_year} Olympics')
    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    st.title('Top stats')
    games = df.Year.nunique() - 1
    events = df.Event.nunique()
    host_cities = df['City'].nunique()
    sports = df.Sport.nunique()
    athletes = df.Name.nunique()
    regions = df.region.nunique()

    col1,col2,col3 = st.columns(3)

    with col1:
        st.subheader('Editions')
        st.title(games)

    with col2:
        st.subheader('Host Cities')
        st.title(host_cities)

    with col3:
        st.subheader('Sports')
        st.title(sports)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader('Athletes')
        st.title(athletes)

    with col5:
        st.subheader('Events')
        st.title(events)

    with col6:
        st.subheader('Nations')
        st.title(regions)

    nations_df = helper.nations_over_time(df)
    st.subheader('Participating nations over the years')
    fig1 = px.line(nations_df, x='index', y='Year', markers=True)
    st.plotly_chart(fig1)

    events_per_year = helper.events_over_time(df)
    st.subheader('No. of events happened over the years')
    fig2 = px.line(events_per_year, x='Years', y='Events', markers=True)
    st.plotly_chart(fig2)

    st.subheader('Sports events over the years')
    sports_events_table = helper.sports_events_over_years(df)

    fig3 = px.imshow(sports_events_table,text_auto=True,width=800,height = 800)
    st.plotly_chart(fig3)
    st.subheader('Top 10 Athletes with highest no. of medals')
    dif_sports = df.Sport.unique().tolist()
    dif_sports.insert(0,'Overall')
    sport = st.sidebar.selectbox('Select Sports',dif_sports)
    top_athletes = helper.most_successfull_athletes(df,sport)
    fig4 = px.bar(top_athletes,x = 'Medal', y = 'Name', color = 'region')
    st.plotly_chart(fig4)

elif user_menu == 'Country wise analysis':
    st.title('Country wise Analysis')
    st.subheader('Country wise tally')
    temp_df = df.dropna(subset='region')
    countries = temp_df.region.unique().tolist()
    countries.sort()
    country  = st.sidebar.selectbox('Select Country',countries)
    country_tally = helper.country_wise_tally(df,country)
    fig5 = px.line(country_tally,x = 'Year', y = 'Medal',markers = True)
    st.plotly_chart(fig5)

    st.subheader('country wise medals for each sport over the years')
    fig6 = helper.country_sports_medals(df,country)
    st.plotly_chart(fig6)

    st.subheader(f'Top 10 athletes of {country}')
    temp_df = helper.most_successfull_athletes_country_wise(df,country)
    st.table(temp_df)

elif user_menu == 'Athlete wise Analysis':
    st.title('Athlete wise Analysis')
    st.subheader('Probability distribution of Age')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    general = athlete_df['Age'].dropna()
    gold = athlete_df[athlete_df.Medal == 'Gold']['Age'].dropna()
    silver = athlete_df[athlete_df.Medal == 'Silver']['Age'].dropna()
    bronze = athlete_df[athlete_df.Medal == 'Bronze']['Age'].dropna()
    fig7 = ff.create_distplot([general, gold, silver, bronze],
                       ['Overall age dist', 'gold medalist dist', 'silver medalist dist', 'bronze medalist dist'],
                       show_hist=False, show_rug=False)
    st.plotly_chart(fig7)
    st.write('This graph show that the likelihood of winning a Gold medal is at peak from age 21 - 25'
             )

    st.subheader('Probability Distribution of Age w.r.t. sports for Gold medalists')
    famous_sports = ['Basketball', 'Judo', 'Tug-Of-War', 'Gymnastics', 'Archery', 'Swimming', 'Shooting',
                     'Weightlifting',
                     'Diving',
                     'Modern Pentathlon',
                     'Handball', 'Canoeing', 'Wrestling', 'Badminton', 'Fencing', 'Boxing', 'Taekwondo', 'Water Polo',
                     'Tennis', 'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Synchronized Swimming', 'Softball', 'Ice Hockey', 'Hockey']
    x = []
    sports = []

    for sport in famous_sports:
        temp_df = df[df.Sport == sport]
        x.append(temp_df[temp_df.Medal == 'Gold'].Age.dropna())
        sports.append(sport)
    fig8 = ff.create_distplot(x, sports, show_hist=False, show_rug=False)
    st.plotly_chart(fig8)

    st.subheader('Weight over Height Comparison for sports')
    all_sports = df.Sport.unique().tolist()
    all_sports.sort()
    all_sports.insert(0,'Overall')
    selected_sport = st.sidebar.selectbox('Select sport', all_sports)
    fig9,ax = plt.subplots()
    temp_df = helper.weight_over_height_comparison(df,selected_sport)
    ax = sns.scatterplot(data = temp_df,x = 'Weight', y = 'Height', hue = 'Medal',
                         style = 'Sex', s = 50)
    st.pyplot(fig9)

    st.subheader('Male vs Female athletes count over the years')
    fig10 = px.imshow(
        athlete_df.pivot_table(index='Sex', columns='Year', values='Name', aggfunc='nunique').fillna(0).astype(int),
        text_auto=True, color_continuous_scale='viridis')
    st.plotly_chart(fig10)

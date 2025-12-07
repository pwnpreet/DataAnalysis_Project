import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
# PAGE CONFIG & LAYOUT------------
st.set_page_config(page_title="Data Analytics App", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://i.imgur.com/YgHUBtu.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# LOAD DATA -----------------------------------
df= pd.read_excel('world_cup_results.xlsx')
matches_df= df.drop_duplicates(subset=['Year', 'Game #']).copy()
matches_df['TotalGoals']= matches_df['Team G'] + matches_df['Opponent G']

# MENU -----------------------
selected= option_menu(
    menu_title=None,
    options=['Home', 'Dataset Info', 'Visuals', 'Insights'],
    icons=['House', 'table', 'bar-chart', 'lightbulb'],
    orientation='horizontal',
    default_index=0,
    styles={
        'container': {'padding': '5px','background-color': '#0a0f1a'},
        'icon': {'color': 'gold','font-size': '20px'},
        'nav-link': {"font-size": "18px","color": "white","margin": "0px","padding": "10px 20px"},
        'nav-link-selected': {"background-color": "#1a2333","color": "gold"}
    },
)

# FUNCTIONS ---------------------
def simple_bar(df, y, x, **kwargs):
    fig= px.bar(df, y=y, x=x, text=x, hover_data=[x], **kwargs)
    fig.update_layout(plot_bgcolor= 'rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig 

def simple_line(df, x, y):
    fig= px.line(df, x=x, y=y, text=y, markers=True)
    fig.update_layout(plot_bgcolor= 'rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig

# HOME --------------------------
if selected == "Home":
    st.title("📈 Welcome to the Data Analytics Web App")
    st.write("""
        This interactive dashboard helps you explore, analyze, and visualize FIFA World Cup match data.

        Use the navigation menu above to:
        - 📄 View dataset structure  
        - 📊 Explore visual insights  
        - 💡 Understand key findings  
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.info("🔍 **Explore match details** — host countries, stadiums, rounds.")
    col2.info("📈 **Analyze trends** — goals over years, match frequency.")
    col3.info("⚽ **Understand performance** — high-scoring teams, goals conceded.")

# DATASET INFO---------------------------
elif selected == "Dataset Info":
    st.title("📝 Dataset Information")
    st.write("Preview, datatypes, null values, summary here...")
    with st.expander("📂 Dataset Preview"):
        st.dataframe(df.head(), use_container_width=True)

    with st.expander("📏 Dataset shape"):
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")

    with st.expander(" ⚡Data Types"):
        st.write(df.dtypes)

    with st.expander("❗Missing Values"):
        st.write(df.isnull().sum())

    with st.expander("📊 Summary Statistics"):
        st.write(df.describe())

# VISUALS -------------------------------
elif selected == "Visuals":
    st.title("📊 Visuals")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ['Host Countries', 'Stadium with Most Games', 'Goals over years', 'Most Goal Conceded', 'Stadiums with most Goals', 'Matches per Round']
    )
    with tab1:
        st.subheader("Which Countries hosted world cup most often?")
        host= matches_df.groupby('Country').size().reset_index(name="MatchesHosted")
        host= host.sort_values('MatchesHosted')
        st.plotly_chart(simple_bar(host,'Country', 'MatchesHosted' ), use_container_width=True)
        st.markdown(
            "- Each bar shows how many World Cup matches were played in that country.\n"
            "- Countries with more matches have hosted more games across tournaments."
        )
    with tab2:
        st.subheader('Which stadium hosts the highest number of games in each country?')
        stadium_count= matches_df.groupby(['Country', 'Stadium']).size().reset_index(name='MatchCount')
        top =stadium_count.loc[stadium_count.groupby('Country')['MatchCount'].idxmax()]
        top= top.sort_values('MatchCount')
        st.plotly_chart(simple_bar(top, 'Country', 'MatchCount', color='Stadium'), use_container_width=True)
        st.markdown(
            "- For each country, we pick the **single stadium** that hosted the most games.\n"
            "- Hover to see the stadium name and match count."
        )
    with tab3:
        st.subheader("How have total goals changed across different World Cups? ")
        yearly= matches_df.groupby('Year')['TotalGoals'].sum().reset_index() 
        st.plotly_chart(simple_line(yearly, 'Year', 'TotalGoals'), use_container_width= True)
        st.markdown(
            "- This line shows how **total goals** scored in a tournament changed over time.\n"
            "- Peaks indicate more attacking tournaments; drops may indicate more defensive eras."
        )
    with tab4:
        st.subheader("Which team conceded the most goals in World Cups?")
        conceded= df.groupby('Team')['Opponent G'].sum().reset_index(name='GoalsConceded')
        top10= conceded.sort_values('GoalsConceded').head(10)
        st.plotly_chart(simple_bar(top10, 'Team', 'GoalsConceded'), use_container_width=True)
        st.markdown(
            "- Each bar shows the **total number of goals conceded** by that team across all World Cups in the dataset.\n"
            "- Teams on top have historically weaker defenses or have played many matches."
        )
    with tab5: 
        st.subheader('Which stadiums have seen most goals scored?')
        goals_stadium= matches_df.groupby('Stadium')['TotalGoals'].sum().reset_index()
        top10= goals_stadium.sort_values('TotalGoals').head(10)
        st.plotly_chart(simple_bar(top10, 'Stadium', 'TotalGoals'), use_container_width=True)
        st.markdown(
            "- These stadiums have witnessed the **highest total number of goals**.\n"
            "- This depends on both how many matches were played and how high-scoring they were."
        )
    with tab6:
        st.subheader('Which rounds has the most matches?')
        rounds= matches_df.groupby('Round').size().reset_index(name='MatchCount')
        st.plotly_chart(simple_bar(rounds.sort_values('MatchCount'), 'Round', 'MatchCount'),use_container_width=True)
        st.markdown(
            "- Group-stage rounds usually appear at the top because they contain many matches.\n"
            "- Knockout rounds (Quarter-finals, Semi-finals, Final) have fewer matches."
        )

elif selected == 'Insights':
    st.title('💡 Key insights')
    # KPI (key performance indicators)
    total_matches= len(matches_df) 
    total_goals= matches_df['TotalGoals'].sum()
    total_countries= matches_df['Country'].nunique()
    total_stadiums= matches_df['Stadium'].nunique()

    col1, col2, col3, col4= st.columns(4)

    col1.metric('Total Matches Played', total_matches)
    col2.metric('Total Goal Scored', total_goals)
    col3.metric('Countries Hosted', total_countries)
    col4.metric('Total Stadium Used', total_stadiums)

    st.markdown('---')
    st.write('🏟️ Top 3 Most Used Stadiums')
    for stadium, count in matches_df['Stadium'].value_counts().head(3).items():
        st.write(f"{stadium}: {count} matches.")

    st.markdown('---')
    st.write("### ⚽ Top 5 Highest Scoring Teams")
    for team, goals in df.groupby('Team')['Team G'].sum().nlargest(5).items():
        st.write(f"{team}: {goals} goals")

    st.markdown("---")
    st.subheader("📄 Summary")
    st.write("""
    - Stadium usage varies significantly across World Cups, with a few iconic stadiums hosting the majority of matches.  
    - Several teams have consistently shown strong attacking performance across the years.  
    - The distribution of matches highlights the global spread and evolution of World Cup tournaments.
    """)
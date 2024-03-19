import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt


st.set_page_config(
    page_title="Exit Poll Statistics for Russian elections 2024: Voting Abroad",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df = pd.read_csv('data/data_exit_polls.csv')

#######################
with st.sidebar:
    st.title('Vote statistics options')
    option_list = ['percent_putin', 'percent_declined',
       'percent_voted_putin_and_declined', 'percent_spoiled']

    selected_option = st.selectbox('Select an option', option_list)
#######################

def make_choropleth(input_df, selected_option):
    choropleth = px.choropleth(input_df, locations="iso_alpha",
                  color=selected_option,
                  hover_name="Country",
                  color_continuous_scale=px.colors.sequential.Reds,
                  projection='robinson')
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


st.markdown('Exit poll results')

choropleth = make_choropleth(df, selected_option)
st.plotly_chart(choropleth, use_container_width=True)


with st.expander('About', expanded=True):
    st.write('''
            - Data: Экзитполлы "Голосуй за рубежом" 
            https://docs.google.com/spreadsheets/d/1HwIbQLXxcB0GAc8DA6uIkYNj0BCXhROKUp7kto9k8Z0/edit#gid=373097824
            ''')

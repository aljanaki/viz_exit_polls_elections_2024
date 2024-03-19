#######################
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Экзитполы 2024 по российским выборам за рубежом",
    layout="wide",
    initial_sidebar_state="expanded")


#######################
# Load data
df = pd.read_csv('data_exit_polls.csv')

#######################
# Sidebar
with st.sidebar:
    st.title('Опции визуализации')

    option_list = ["Испорченный бюллетень (%)", "Путин (%)", "Не хочу отвечать (%)", "Даванков (%)", "Слуцкий (%)", "Харитонов (%)"]
    option_list_column_names = ['percent_spoiled', 'percent_putin', 'percent_declined',
       'davankov_perc', 'slutskiy_perc', 'haritonov_perc']

    selected_option = st.selectbox('Выбери статистику для визуализации', option_list)

#######################
# Plots
def createHoverTexts(df):
    '''
    Auxilliary function, creates hover text for each country with sorted statistics
    :param df:
    :return:
    '''
    df['Hovertext'] = ''
    for index, row in df.iterrows():
        dic = {'Даванков': row['davankov_perc'], "Слуцкий": row['slutskiy_perc'], "Харитонов": row['haritonov_perc'],
               "Путин": row['percent_putin'], 'Испорчено': row['percent_spoiled'],
               "Отказались отвечать": row['percent_declined']}
        sortedDict = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
        texts = []
        texts.append(row['Country_rus'])

        for item in sortedDict.items():
            texts.append(f"{item[0]}: {str(item[1])}%")
        texts.append(f"Опрошено человек: {row['answers_collected']}")
        hovertext = '<br>'.join(texts)
        df.at[index, 'Hovertext'] = hovertext
    return df


# Choropleth map
def make_choropleth(input_df, selected_option, option_list, option_list_column_names):
    input_df = createHoverTexts(input_df)

    choropleth = px.choropleth(input_df, locations="iso_alpha",
                  color= option_list_column_names[option_list.index(selected_option)],
                  hover_name="Hovertext",
                  color_continuous_scale=px.colors.sequential.Blues,
                  projection='robinson',
                 hover_data={option_list_column_names[option_list.index(selected_option)]: False, 'iso_alpha': False})

    choropleth.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width = 800,
        height = 800
    )

    return choropleth

st.markdown('''### Результаты экзит полов


Наведите курсор на страну, чтобы увидеть подробности. 
''')

choropleth = make_choropleth(df, selected_option, option_list, option_list_column_names)
st.plotly_chart(choropleth, use_container_width=True)


with st.expander('Источник данных', expanded=True):
    st.write('''
            Экзитполлы "Голосуй за рубежом" 
            https://docs.google.com/spreadsheets/d/1HwIbQLXxcB0GAc8DA6uIkYNj0BCXhROKUp7kto9k8Z0/edit#gid=373097824
            ''')

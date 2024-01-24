import streamlit as st
import pandas as pd

import plotly.express as px


from typing import Iterable

from lib.filterwidget import OurFilter
from toolz import pluck

MY_TABLE = "CUSTOMERS"

def _get_active_filters() -> filter:
    return filter(lambda _: _.is_enabled, st.session_state.filters)

def _is_any_filter_enabled() -> bool:
    return any(pluck("is_enabled", st.session_state.filters))

def _get_human_filter_names(_iter: Iterable) -> Iterable:
    return pluck("human_name", _iter)

def draw_sidebar():
    """Should include dynamically generated filters"""

    with st.sidebar:
        selected_filters = st.multiselect(
            "Select which filters to enable",
            list(_get_human_filter_names(st.session_state.filters)),
            [],
        )
        for _f in st.session_state.filters:
            if _f.human_name in selected_filters:
                _f.enable()

        if _is_any_filter_enabled():
            with st.form(key="input_form"):

                for _f in _get_active_filters():
                    _f.create_widget()
                st.session_state.clicked = st.form_submit_button(label="Submit")
        else:
            st.write("Please enable a filter")

if __name__ == "__main__":
    # Initialize the filters
    session = init_connection()
    OurFilter.session = session
    OurFilter.table_name = MY_TABLE

    st.session_state.filters = (
        OurFilter(
            human_name="Current customer",
            table_column="is_current_customer",
            widget_id="current_customer",
            widget_type=st.checkbox,
        ),
        OurFilter(
            human_name="Tenure",
            table_column="years_tenure",
            widget_id="tenure_slider",
            widget_type=st.select_slider,
        ),
        OurFilter(
            human_name="Weekly workout count",
            table_column="average_weekly_workout_count",
            widget_id="workouts_slider",
            widget_type=st.select_slider,
        ),
    )

    draw_sidebar()


def cat_questions(question, type):
    return type in question

def iter(question):
    cate_return = ""
    categoy = []
    wh = ["why","when","what","who","where","which","how"]
    for i in wh:
        cate = cat_questions(question,i)
        categoy.append(cate)
    #print(len(categoy))
    if(categoy[0]==True):
        cate_return = wh[0]
    elif(categoy[1]==True):
        cate_return = wh[1]
    elif(categoy[2]==True):
        cate_return = wh[2]
    elif(categoy[3] == True):
        cate_return = wh[3]
    elif(categoy[4] == True):
        cate_return = wh[4]
    elif(categoy[5] == True):
        cate_return = wh[5]
    elif(categoy[6] == True):
        cate_return = wh[6]
    else:
        cate_return = "None"
    return cate_return



content1 = st.container()
content2 = st.container()

df = pd.read_csv('data.csv')

df['question_category'] = df['question_text'].apply(lambda x:iter(x))

cate_count = df['question_category'].value_counts()

cate_count = cate_count.reset_index()
print(cate_count)
# Rename the columns
cate_count.columns = ['value', 'count']

st.write("hellow world")
with content1:
    st.title("Row Level look")
    fig = px.pie(cate_count,values='count',names='value')
    st.write(fig)

with content2:
    st.title("Row Level look")
    st.dataframe(df,use_container_width=True,hide_index=True)



import streamlit as st
import pandas as pd

import plotly.express as px


from toolz import pluck


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
content3 = st.container()

df = pd.read_csv('data.csv')

df['question_category'] = df['question_text'].apply(lambda x:iter(x))

cate_count = df['question_category'].value_counts()

cate_count = cate_count.reset_index()
print(cate_count)
# Rename the columns
cate_count.columns = ['value', 'count']

with content1:
    st.write("Hey, Imesh HERE!!!!!!")

    st.title("Questions By Categories")
    fig = px.pie(cate_count,values='count',names='value')
    st.write(fig)

    

with content2:
    st.title("Row Level look")

    u_in = st.text_input("Search title?")

    new_df=df[['document_title','question_text','short_answer1','short_answer2','short_answer3','short_answer4']]
    if(len(u_in)>0):
        new_df = new_df[new_df['document_title'].str.lower().str.contains(u_in.lower())]

    st.dataframe(new_df,use_container_width=True,hide_index=True)

with content3:
    st.title("Breif on the task")
    st.write("As an initial step of the assignment the data set was examined")
    st.write("However I was able examin some of the issues in the dataset")
    st.write("          Retreiving the original text from token was inconsitent ")
    st.write("          Reading annotations from start_byte and end_byte was unsuccessfull")
    st.write("I was unable to make meaningfull retreival with annotations due to above reasons")






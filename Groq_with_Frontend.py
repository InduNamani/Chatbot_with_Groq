import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
##Load the environment variables
load_dotenv()
#Langsmith Tracking

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

#Prompt Template

prompt=ChatPromptTemplate(
    [
    ("system","You are a helpful assistant. Please respond to the user"),
    ("user","Question:{question}")
    ]
)
#Function to generate a resplonse

def generate_resplonse(question,model_name,temperature,max_tokens):
    llm=ChatGroq(
        model=model_name,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens
    )    

    output_parser=StrOutputParser()
    chain=chain = prompt | llm | output_parser
    answer=chain.invoke({"question":question})
    return answer
    

st.title("Q&A Chatbot with Groq")
st.sidebar.title("Settings")

model_name=st.sidebar.selectbox(
    "Select Groq Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "groq/compoud"
    ]
)

#Parameters

temperature=st.sidebar.slider(
    "Temeperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7
)

max_tokens=st.sidebar.slider(
    "Maxtokens",
    min_value=50,
    max_value=1000,
    value=300
)

#User Input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_resplonse(
        user_input,
        model_name,
        temperature,
        max_tokens
    )

    st.write(response)
else:
    st.write("Please provide user input.")



   
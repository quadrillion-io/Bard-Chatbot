import streamlit as st
from streamlit_chat import message
from bardapi import Bard
import json

# open the config file
with open('config.json') as config_file:
    data = json.load(config_file)

# store the bard api key in a variable
bard_api_key = data["BARD_API_KEY"]

# initialize the bard api
bard = Bard(token=bard_api_key, timeout= 30)

def generate_response(prompt):
    # this function takes in a prompt, and then calls the bard api to get the bard response
    history = ""
    for user_response, bard_response in zip(st.session_state['user_responses'], st.session_state['bard_responses']):
        history += f"User: {user_response}\n"
        history += f"Bard Response: {bard_response}\n"

    response = bard.get_answer(f"Conversation History: {history}\n {prompt}")   

    return response["content"]

def on_btn_click():
    # this function clears the session state
    del st.session_state['user_responses']
    del st.session_state['bard_responses']

def on_input_change():
    # this function is called when the user inputs something in the text input field
    # it stores the user input in the session state, and then calls the generate_response function
    # to get the bard response.
    # it then appends the user input and bard response to the session state, and then clears the
    # user input field.
    
    user_input = st.session_state.user_input
    output = generate_response(user_input)
    st.session_state.user_responses.append(user_input)
    st.session_state.bard_responses.append(output)
    st.session_state["user_input"] = ""

# create the title for the page
st.title("Bard Chatbot")

# create a button to clear the session state (chat history)
st.button("New Topic", on_click=on_btn_click)

if 'bard_responses' not in st.session_state:
    st.session_state['bard_responses'] = []

if 'user_responses' not in st.session_state:
    st.session_state['user_responses'] = []

# create the text input field
with st.container():
    st.text_input("User Response:", on_change=on_input_change, key="user_input")

# show a loading spinner while the bard api is getting the response
# then show the chat history
with st.spinner("Loading..."):   
    if st.session_state['bard_responses']:

        for i in range(len(st.session_state['bard_responses'])-1, -1, -1):
            message(st.session_state["bard_responses"][i], key=str(i))
            message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user')
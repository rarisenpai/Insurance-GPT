import streamlit as st
from utils import index_data, query_data
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="A chatbot for insurance")
st.title("A chatbot for insurance")
with st.sidebar:
    choice = st.selectbox("Select what you want to do?", ["Upload document", "Ask a question"])

if choice == "Upload document":
    st.subheader("Please upload the document you want questions answered from?")
    # Upload the document
    uploaded_files = st.file_uploader("Upload Document", type=["pdf", "docx","txt"], accept_multiple_files=True)

    if uploaded_files is not None:
        # Create a directory to save uploaded files
        os.makedirs("data", exist_ok=True)

        for uploaded_file in uploaded_files:
            # Save each uploaded file to the "data" directory
            file_path = os.path.join("data", uploaded_file.name)
            with open(file_path, "wb") as file:
                file.write(uploaded_file.getvalue())


elif choice == "Ask a question":
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["How may I help you?"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi!']

    input_container = st.container()
    colored_header(label='', description='', color_name='blue-30')
    response_container = st.container()

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    def generate_response(prompt):
        response = query_data(index, user_input)
        return response

    ## Applying the user input box
    with input_container:
        user_input = get_text()
    
    index = index_data("data")

    ## Conditional display of AI generated responses as a function of user provided prompts
    with response_container:
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(str(st.session_state["generated"][i]), key=str(i))

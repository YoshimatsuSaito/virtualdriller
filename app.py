import io

import streamlit as st

from utils.utils import extract_text_from_ppt
from utils.prompt_manager import Driller

st.set_page_config(layout="wide")
st.title("Virtual Driller")


if "started" not in st.session_state:
    st.session_state.started = False

if "driller" not in st.session_state:
    st.session_state.driller = None

if "client_information" not in st.session_state:
    st.session_state.client_information = None


client_information = st.text_area("Please input the client information")


if st.button("Start"):
    st.session_state.client_information = client_information
    driller = Driller(st.session_state.client_information)
    st.session_state.started = True
    st.session_state.driller = driller
    st.session_state.client_information = client_information

if st.session_state.started and st.session_state.client_information == client_information:
    cols = st.columns(2)
    with cols[0]:
        user_input = st.text_area("Please input the presentation")
        if st.button("Send", key="text"):
            st.session_state.driller.hear(user_input)
            st.session_state.driller.drill()

    with cols[1]:
        uploaded_file = st.file_uploader("Choose a PowerPoint file", type=["pptx"])
        if uploaded_file is not None:
            with io.BytesIO(uploaded_file.getbuffer()) as ppt_file:
                user_input = extract_text_from_ppt(ppt_file)
            if st.button("Send", key="ppt"):
                st.session_state.driller.hear(user_input)
                st.session_state.driller.drill()

    for history in st.session_state.driller.list_message[1:]:
        st.markdown("---")
        st.markdown(history["content"])

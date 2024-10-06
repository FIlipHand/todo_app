import streamlit as st
import requests
import json


@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()


columns = st.columns(3)

elements_raw = requests.get(url="http://0.0.0.0:8000/tasks/")
elements = json.loads(elements_raw.text)

for idx, elem in enumerate(elements):
    with columns[idx % 3].container(height=250):
        st.title(elem["title"])
        st.text(elem["description"])
        # Create a button for each tile
        if st.button("Details", key=idx):
            vote(elem)

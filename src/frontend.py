import streamlit as st
from datetime import datetime
import requests
import json


def fetch_tasks():
    elements_raw = requests.get(url="http://127.0.0.1:8000/tasks/get_all_tasks")
    return json.loads(elements_raw.text)


def tmp():
    task_title = st.text_input(label="Task title")
    task_disc = st.text_area(label="Description")
    task_priority = st.slider("Select priority", 0, 10, 5)


@st.dialog("Task details")
def task_details(task):
    st.title(f"{task['title']}")
    st.write(task["description"])
    st.write(
        f"Started: {datetime.strptime(task['start_date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y at %I:%M:%S %p')}"
    )
    st.write(f"Status: {task['status']}")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Close task"):
            requests.get(url="http://127.0.0.1:8000/tasks/close_task", data=json.dumps({"id": task["id"]}))
            st.rerun()
    with col2:
        if st.button("Print"):
            print("Jeszcze tutaj nic się nie dzieje :D")
    if task["close_date"] is None:
        if col3.button("Add subtask"):
            task_title = st.text_input(label="Task title")
            task_disc = st.text_area(label="Description")
            task_priority = st.slider("Select priority", 0, 10, 5)
            task_dict = {
                "title": task_title,
                "description": task_disc,
                "priority": task_priority,
                "parent_id": task["id"],
            }
            if st.button("Create task"):
                requests.post(url="http://127.0.0.1:8000/tasks/create_task", data=json.dumps(task_dict))


@st.dialog("Create new task")
def create_task():
    st.title("Creating new items")
    task_title = st.text_input(label="Task title")
    task_disc = st.text_area(label="Description")
    task_priority = st.slider("Select priority", 0, 10, 5)
    elements = fetch_tasks()
    possible_parents = (elem for elem in elements if elem["close_date"] is None)
    parent = st.selectbox("Parent task", possible_parents, index=None)
    if st.button("Submit"):
        task_dict = {"title": task_title, "description": task_disc, "priority": task_priority, "parent_id": None}
        requests.post(url="http://127.0.0.1:8000/tasks/create_task", data=json.dumps(task_dict))
        st.rerun()


st.sidebar.title("Quick tools")
if st.sidebar.button("Create task"):
    create_task()

select_filter = "active"
if st.sidebar.button("Show all tasks"):
    select_filter = "all"
if st.sidebar.button("Show active tasks"):
    select_filter = "active"
if st.sidebar.button("Show closed tasks"):
    select_filter = "closed"

columns = st.columns(3)

elements = fetch_tasks()

match select_filter:
    case "active":
        elements = [elem for elem in elements if elem["close_date"] is None]
    case "closed":
        elements = [elem for elem in elements if elem["close_date"] is not None]
    case _:
        pass


for idx, elem in enumerate(elements):
    with columns[idx % 3].container(height=250):
        task_prefix = ""
        if elem["close_date"] is not None:
            task_prefix = ":red[[CLOSED]]"
        st.markdown(f"##### {task_prefix} {elem['title']}")
        st.text(elem["description"])
        # Create a button for each tile
        if st.button("Details", key=idx):
            task_details(elem)

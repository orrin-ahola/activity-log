import streamlit as st
import os
import json
import uuid
from datetime import datetime



st.set_page_config(layout="wide")

# Inject custom CSS for fixed form and scrollable list
st.markdown("""
    <style>
        /* Fixed form container */
        div[data-testid="stForm"] {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: white;
            z-index: 999;
            padding: 10px 75px; /* Adjust top/bottom and left/right padding */
            border-bottom: 2px solid #ddd;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Scrollable list container */
        .scrollable-list {
            margin-top: 150px; /* Space for the fixed form */
            height: calc(100vh - 160px); /* Remaining vertical space */
            overflow-y: auto;
            padding: 20px 300px !important; /* Top/Bottom and Left/Right padding */
        }
        
        /* Inner wrapper for padding */
        .scrollable-list .inner {
            padding: 20px 300px !important;
        }
    </style>
""", unsafe_allow_html=True)


DATA_FILE = os.path.join(os.path.dirname(__file__), "entries.json")

# Initialize session state
if "entries" not in st.session_state:
    st.session_state.entries = []

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def parse_datetime_str(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def delete_entry(entry_id):
    st.session_state.entries = [x for x in st.session_state.entries if x["id"] != entry_id]
    save_data(st.session_state.entries)  # Save updated data

def edit_entry(entry_id):
    st.session_state.entries = [x for x in st.session_state.entries if x["id"] != entry_id]
    save_data(st.session_state.entries)  # Save updated data

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load entries on startup
if not st.session_state.entries:
    st.session_state.entries = load_data()
    st.session_state.entries.sort(key=lambda x: parse_datetime_str(x["date"], x["time"]), reverse=True)

# App layout
st.title("Personal Activity Log")

# Two-column form layout
with st.form(key="entry_form", clear_on_submit=True):
    st.subheader("Add New Entry")
    col1, col2 = st.columns([1, 5])  # Column proportions: 1/6 and 5/6

    # Left column: Date, Time, Submit Button
    with col1:
        current_date = st.date_input("Date", value=datetime.now())
        current_time = st.time_input("Time", value=datetime.now().time())
        submitted = st.form_submit_button("Submit")

    # Right column: Activity text area
    with col2:
        activity_text = st.text_area("Activity:", height=150)

    if submitted:
        # Add new entry
        new_entry = {
            "id": str(uuid.uuid4()),
            "date": current_date.strftime("%Y-%m-%d"),
            "time": current_time.strftime("%H:%M"),
            "text": activity_text.strip()
        }
        st.session_state.entries.append(new_entry)
        st.session_state.entries.sort(key=lambda x: parse_datetime_str(x["date"], x["time"]), reverse=True)
        save_data(st.session_state.entries)
        st.success("New entry added!")

# Display Entries in a Nice Layout
# Scrollable container for the entries list
st.markdown('<div class="scrollable-list"><div class="inner">', unsafe_allow_html=True)

st.subheader("All Entries (Most Recent First)")

if st.session_state.entries:
    # Header row
    header_cols = st.columns([0.7, 0.4, 6])
    header_cols[0].markdown("**Date**")
    header_cols[1].markdown("**Time**")
    header_cols[2].markdown("**Activity**")

    # Data rows
    for e in st.session_state.entries:
        row = st.columns([0.7, 0.4, 5, 0.5, 0.5])
        row[0].write(e["date"])
        row[1].write(e["time"])
        row[2].write(e["text"])
        row[3].button("✏️️", key=f"edit_{e['id']}", on_click=edit_entry, args=(e["id"],))
        row[4].button("🗑️", key=f"delete_{e['id']}", on_click=delete_entry, args=(e["id"],))

    save_data(st.session_state.entries)  # Update JSON file
else:
    st.write("No entries yet. Add something above!")

st.markdown('</div></div>', unsafe_allow_html=True)

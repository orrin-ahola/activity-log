import streamlit as st

st.markdown("""
    <style>
        /* Set the entire app background color to light blue */
        .stApp {
            background-color: lightblue;
        }

        /* Fixed form container with a white background */
        div[data-testid="stForm"] {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: white; /* Keeps the form background white */
            z-index: 999;
            padding: 10px;
            border-bottom: 2px solid #ddd;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Scrollable list container below the fixed form */
        .scrollable-list {
            margin-top: 100px; /* Space for fixed form */
            height: calc(100vh - 110px);
            overflow-y: auto;
            background-color: lightblue; /* Ensures the list matches app background */
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Fixed Form Section
with st.container():
    st.markdown('<div data-testid="stForm">', unsafe_allow_html=True)
    with st.form("top_form"):
        st.write("### Static Form Section")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("First Name")
        with col2:
            st.text_input("Last Name")
        with col3:
            st.number_input("Age", min_value=0, max_value=100)
        submit_button = st.form_submit_button("Submit")
    st.markdown('</div>', unsafe_allow_html=True)

# Scrollable List Below
st.markdown('<div class="scrollable-list">', unsafe_allow_html=True)
st.write("### Scrollable List Section")
for i in range(1, 51):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        st.write(f"**Item {i}**")
    with col2:
        st.write(f"Detail {i}")
    with col3:
        st.write(f"Other Info {i}")
    with col4:
        st.button("Edit ✏️", key=f"edit_{i}")
        st.button("🗑️", key=f"delete_{i}")
st.markdown('</div>', unsafe_allow_html=True)

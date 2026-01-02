import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox

# Load Excel data 
@st.cache_data
def load_data():
    return pd.read_excel("Lookup_Database.xlsx")

df = load_data()

# Function triggered on every keystroke
def search_addresses(searchterm: str):
    # Require 3 characters for address searches to narrow down results faster
    if not searchterm or len(searchterm) < 3:
        return []
    
   
    # case=False makes it non-case-sensitive
    mask = df['ADDRESS'].str.contains(searchterm, case=False, na=False)
    matches = df[mask]['ADDRESS'].unique().tolist()
    
    # Return top 10 matches to keep the dropdown clean
    return matches[:10]

st.title("Address Search")

# The dynamic search component
selected_address = st_searchbox(
    search_addresses,
    key="address_search",
    placeholder="Type an address",
)

# Display the full row data when an address is selected
if selected_address:
    st.markdown(f"### Result for: **{selected_address}**")
    result_data = df[df['ADDRESS'] == selected_address]
    st.dataframe(result_data, use_container_width=True)
else:
    st.info("Start typing at least 3 characters of an address to see matches.")

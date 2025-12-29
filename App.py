import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox

# Load Excel data (cached for 2025 performance standards)
@st.cache_data
def load_data():
    # Ensure your Excel file is named 'database.xlsx' in the same folder
    return pd.read_excel("Axle_Lookup.xlsx")

df = load_data()

# Function triggered on every keystroke
def search_addresses(searchterm: str):
    # Require 3 characters for address searches to narrow down results faster
    if not searchterm or len(searchterm) < 3:
        return []
    
    # Filter the 'Address' column (Ensure your Excel header is exactly 'Address')
    # case=False makes it non-case-sensitive
    mask = df['Address'].str.contains(searchterm, case=False, na=False)
    matches = df[mask]['Address'].unique().tolist()
    
    # Return top 10 matches to keep the dropdown clean
    return matches[:10]

st.title("📍 Address Search Portal")

# The dynamic search component
selected_address = st_searchbox(
    search_addresses,
    key="address_search",
    placeholder="Type an address (e.g., 123 Main St)...",
)

# Display the full row data when an address is selected
if selected_address:
    st.markdown(f"### Result for: **{selected_address}**")
    result_data = df[df['Address'] == selected_address]
    st.dataframe(result_data, use_container_width=True)
else:
    st.info("Start typing at least 3 characters of an address to see matches.")

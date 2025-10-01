import pandas as pd
import streamlit as st

# Load Excel file
file_path = "moza saee mirali.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

st.title("Excel Data Filter Tool")

# Create search boxes for each column
filters = {}
for col in df.columns:
    filters[col] = st.text_input(f"Search in {col}")

# Apply filters
filtered_df = df.copy()
for col, search_value in filters.items():
    if search_value:
        filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(search_value, case=False, na=False)]

st.write("### Filtered Data", filtered_df)

# Option to download filtered data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)

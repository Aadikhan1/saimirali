import pandas as pd
import streamlit as st

file_path = "moza saee mirali.xlsx"

# Force openpyxl engine
df = pd.read_excel(file_path, sheet_name="Sheet1", engine="openpyxl")

st.title("Excel Data Filter Tool")

filters = {}
for col in df.columns:
    filters[col] = st.text_input(f"Search in {col}")

filtered_df = df.copy()
for col, search_value in filters.items():
    if search_value:
        filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(search_value, case=False, na=False)]

st.write("### Filtered Data", filtered_df)

# Download option
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

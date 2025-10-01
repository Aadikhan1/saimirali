import pandas as pd
import streamlit as st

st.title("Excel Data Filter Tool")

# Upload file
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Handle Excel or CSV
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")

    st.success("File uploaded successfully!")
    st.write("### Preview of Data", df.head())

    # Search filters for each column
    filters = {}
    for col in df.columns:
        filters[col] = st.text_input(f"Search in {col}")

    # Apply filters
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
else:
    st.info("Please upload an Excel or CSV file to begin.")

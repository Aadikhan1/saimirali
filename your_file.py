import pandas as pd
import streamlit as st

st.title("Sai Mirali Owners Data Tool & Khewat Selection")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")
            except ImportError:
                st.error("`openpyxl` is not installed. Please upload a CSV file instead.")
                st.stop()

        st.success("File uploaded successfully!")
        st.write("### Preview of Data", df.head())

        # --- Khewat selection ---
        if "khewat" in df.columns:
            khewat_option = st.selectbox("Select Khewat", options=["All"] + sorted(df["khewat"].dropna().unique().astype(str).tolist()))
        else:
            khewat_option = "All"

        # --- Search filters (only specific columns) ---
        filters = {}
        for col in ["first name", "last name", "cnic no"]:
            if col in df.columns:
                filters[col] = st.text_input(f"Search in {col}")

        # --- Apply filters ---
        filtered_df = df.copy()

        # Apply khewat filter
        if khewat_option != "All":
            filtered_df = filtered_df[filtered_df["khewat"].astype(str) == str(khewat_option)]

        # Apply search filters
        for col, search_value in filters.items():
            if search_value:
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(search_value, case=False, na=False)]

        # Show results
        st.write("### Filtered Data", filtered_df)

        # --- Download filtered data ---
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(filtered_df)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload an Excel (.xlsx, .xls) or CSV file to begin.")

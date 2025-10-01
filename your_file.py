import pandas as pd
import streamlit as st

st.title("Sai Mirali Owners Data Tool")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")
            except ImportError:
                st.error("`openpyxl` is not installed in this environment. Please upload a CSV file instead.")
                st.stop()

        st.success("File uploaded successfully!")
        st.write("### Preview of Data", df.head())

        # --- Text filters (First Name, Last Name, NIC) ---
        search_cols = ["First Name", "Last Name", "NIC"]
        filters = {}

        for col in search_cols:
            if col in df.columns:
                filters[col] = st.text_input(f"Search in {col}")

        filtered_df = df.copy()
        for col, search_value in filters.items():
            if search_value:
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(search_value, case=False, na=False)]

        # --- Reorder columns ---
        ordered_cols = [c for c in ["SNo", "Mauza", "First Name", "Relation", "Last Name", "NIC", "khewat no"] if c in filtered_df.columns]
        remaining_cols = [c for c in filtered_df.columns if c not in ordered_cols]
        filtered_df = filtered_df[ordered_cols + remaining_cols]

        st.write("### Filtered Data", filtered_df)

        # --- Khewat no selection ---
        if "khewat no" in df.columns:
            # Keep as string
            df["khewat no"] = df["khewat no"].astype(str)

            # Custom sort: main numbers first, then sub-numbers
            def khewat_sort_key(k):
                parts = k.split("/")
                try:
                    main = int(parts[0])
                except:
                    main = float("inf")
                sub = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                return (main, sub)

            khewat_list = sorted(df["khewat no"].dropna().unique().tolist(), key=khewat_sort_key)

            selected_khewat = st.selectbox("Select Khewat No to view all records", ["None"] + khewat_list)

            if selected_khewat != "None":
                khewat_df = df[df["khewat no"] == selected_khewat]

                # Reorder for khewat result
                ordered_cols_k = [c for c in ["SNo", "Mauza", "First Name", "Relation", "Last Name", "NIC", "khewat no"] if c in khewat_df.columns]
                remaining_cols_k = [c for c in khewat_df.columns if c not in ordered_cols_k]
                khewat_df = khewat_df[ordered_cols_k + remaining_cols_k]

                st.write(f"### All Records for Khewat No {selected_khewat}", khewat_df)

                # Download Khewat result
                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode("utf-8")

                csv_khewat = convert_df(khewat_df)
                st.download_button(
                    label=f"Download all records for Khewat No {selected_khewat}",
                    data=csv_khewat,
                    file_name=f"khewat_{selected_khewat}.csv",
                    mime="text/csv",
                )

        # --- Download filtered data (from text search) ---
        @st.cache_data
        def convert_df_all(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df_all(filtered_df)
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

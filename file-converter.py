import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert.")

files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing Values Filled")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty():
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        output = BytesIO()  # ✅ Corrected output type
        new_name = file.name.replace(ext, "csv" if format_choice == "CSV" else "xlsx")

        if st.button(f"Download {file.name} as {format_choice}"):
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            output.seek(0)  # ✅ Needed to reset file pointer
            st.download_button("Download File", file_name=new_name, data=output, mime=mime)  # ✅ Fixed file_name

        st.success("Processing Completed!")

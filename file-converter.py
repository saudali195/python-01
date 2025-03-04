import streamlit as st
import pandas as pd
from io import BytesIO

# ✅ Move this to the top before any other Streamlit commands!
st.set_page_config(page_title="File Converter", layout="wide")

# 🔹 Add a watermark using CSS
st.markdown(
    """
    <style>
    body::before {
        content: "XYRON";  /* Change to 'SaudAli' if you want */
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 80px;
        color: rgba(200, 200, 200, 0.1);
        z-index: -1;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("File Converter & Cleaner 🔥")
st.markdown("### Developed by **XYRON** 🚀")

# File Upload Section
files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

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

        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        output = BytesIO()
        if st.button(f"Download {file.name} as {format_choice}"):
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download File", file_name=new_name, data=output, mime=mime)

st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 10px; color: grey;">
        <b>© XYRON | SaudAli</b>
    </div>
    """,
    unsafe_allow_html=True
)

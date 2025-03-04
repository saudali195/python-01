import streamlit as st
import pandas as pd
from io import BytesIO

# ✅ Set page configuration
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
        
        # ✅ Load the file safely
        try:
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
            continue  # Skip this file and move to the next
        
        st.subheader(f"{file.name} Preview")
        st.dataframe(df.head())

        # ✅ Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        # ✅ Fill Missing Values
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            numeric_cols = df.select_dtypes(include=["number"])
            if not numeric_cols.empty:
                df.fillna(numeric_cols.mean(), inplace=True)
                st.success("Missing Values Filled")
                st.dataframe(df.head())
            else:
                st.warning("No numeric columns found to fill missing values.")

        # ✅ Select Columns
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # ✅ Show Chart (Fix: Correct `.empty` check)
        numeric_data = df.select_dtypes(include="number")
        if st.checkbox(f"Show Chart - {file.name}") and not numeric_data.empty:
            st.bar_chart(numeric_data.iloc[:, :2])  # Select first 2 numeric columns to avoid errors

        # ✅ File Format Conversion
        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        output = BytesIO()
        if st.button(f"Download {file.name} as {format_choice}"):
            try:
                if format_choice.lower() == "csv":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = file.name.replace(ext, "csv")
                else:
                    df.to_excel(output, index=False, engine='openpyxl')
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("Download File", file_name=new_name, data=output, mime=mime)
            except Exception as e:
                st.error(f"Error converting file: {e}")

st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 10px; color: grey;">
        <b>© XYRON | SaudAli</b>
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import TextSummary


st.title(":blue[File summarizer]")

st.header('Upload your file here')
uploaded_file = st.file_uploader("Choose a file",type=["pdf"])

if uploaded_file is not None:
    pdf_text = TextSummary.convert(uploaded_file)

    # Display the PDF content
    summary=TextSummary.summarize(pdf_text)
    c=st.container()
    c.write(summary)
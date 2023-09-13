import streamlit as st
import openai
import PyPDF2
import tempfile 
import os

# Set your OpenAI API key
openai.api_key = "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"

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    pdf_text = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    with open(temp_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages) ):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
    
    # Remove the temporary PDF file
    os.remove(temp_pdf_path)

    return pdf_text

# Streamlit app
def main():
    st.title("Financial Report Commentary Generator")

    # File upload widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Read PDF content
        pdf_text = extract_text_from_pdf(uploaded_file)

        # Generate commentary
        prompt = f"""
        Please analyze the provided financial reports for Prudent Asset Management, including the Profitability Report and the P&L Report, and generate a comprehensive commentary. Compare the data between Jan 2023 and Feb 2023 and provide insights on the changes in key financial metrics. Specifically, analyze the performance of the Profitability Report and its relationship with the P&L Report.

        {pdf_text}

        Commentary:
        """

        # Generate commentary using OpenAI GPT-3.5 Turbo
        response = openai.Completion.create(
            engine="text-davinci-003",  # Change to "gpt-3.5-turbo"
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop="\n"
        )

        # Extract the generated commentary from the response
        commentary = response.choices[0].text.strip()

        # Display the generated commentary
        st.header("Generated Commentary")
        st.text_area("Commentary:", value=commentary, height=400)

if __name__ == "__main__":
    main()

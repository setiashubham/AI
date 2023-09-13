import streamlit as st
import openai
import tempfile
import os
import PyPDF2
import pandas as pd

# Define your OpenAI API key
openai_api_key = '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'

# Function to analyze and generate commentary
def generate_commentary(file_contents):
    # You can customize the prompt based on your specific use case
    prompt = """
Please analyze the provided financial reports for Prudent Asset Management, including the Profitability Report and the P&L Report, and generate a comprehensive commentary. Compare the data between Jan 2023 and Feb 2023 and provide insights on the changes in key financial metrics. Specifically, analyze the performance of the Profitability Report and its relationship with the P&L Report.

Profitability Report ($m):

1. Start by comparing "Total Revenue" in Jan 2023 and Feb 2023. Highlight any percentage changes and provide reasons for the changes, such as shifts in specific revenue streams.

2. Analyze "Total Costs" for the same period. Identify any significant changes and the contributing factors behind these changes.

3. Examine the "Profit/(Loss)" and discuss the reasons for any fluctuations between Jan and Feb 2023.

4. Evaluate the "Margin (%)" and provide insights into the profitability trend.

5. Finally, discuss the impact of changes in "Net Earnings" and the key drivers.

P&L Report ($m):

1. Compare the components of the P&L Report, such as "Management Fees," "Administrative Fees," "Third-Party Revenue," "Asset-Based Distribution Fees," and "Fund Expenses" between Jan and Feb 2023. Highlight percentage changes and reasons for these changes.

2. Examine the "Total Asset-Based Revenue" and its relationship with "Management Fees" and other revenue sources. Discuss any notable shifts.

3. Analyze "Performance Fees," "Other Distribution Fees," and "Other Revenue" for any significant variations.

4. Calculate the "Total Revenue" based on the P&L Report and discuss how it correlates with the "Total Revenue" in the Profitability Report.

5. Finally, compare "Total Costs" in the P&L Report for Jan and Feb 2023 and provide insights into any changes.

Please ensure that the commentary is structured, informative, and includes both quantitative data and qualitative explanation and is only based on the document provided.


with the same name, create separate answers for each. Only include information found in the results 
Don't add any additional information. Make sure the answer is correct and don't output false content. 
If the text does not relate to the query, simply state 'Text Not Found in PDF'. 
Ignore outlier and Search results which has nothing to do with the question. Only answer what is asked.
answer should be short and concise. Answer step-by-step.
"""
    # Call the OpenAI GPT model to generate commentary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message["content"]

# Initialize Streamlit app
def main():
    st.title("File Analysis and Commentary Generator")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        # Read the file contents
        file_contents = ""
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == ".pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                file_contents += page.extract_text()
        elif file_extension in [".xlsx", ".xls"]:
            df = pd.read_excel(uploaded_file)
            file_contents = df.to_string(index=False)
        elif file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
            file_contents = df.to_string(index=False)
        else:
            file_contents = uploaded_file.getvalue().decode()

        # # Display the file contents
        # st.subheader("File Contents:")
        # #st.text(file_contents)

        if st.button("Generate Commentary"):
            # Generate commentary using OpenAI GPT model
            commentary = generate_commentary(file_contents)

            # Display the commentary
            st.subheader("Generated Commentary:")
            st.write(commentary)

if __name__ == "__main__":
    main()

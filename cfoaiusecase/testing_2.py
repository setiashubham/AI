'''import streamlit as st
import openai
import tempfile
import os
import PyPDF2
import pandas as pd

# Define your OpenAI API key
openai_api_key = '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'

# Function to analyze and generate commentary
def generate_commentary(file_contents, user_question):
    # You can customize the prompt based on your specific use case
    prompt = f"""Please analyze the following document and provide commentary by doing comparison on month on month basis, comparison on Year to date(YTD) basis, comparison on year to year(YTY) basis, and any other combinations possible. Please provide the difference and percentage change (please write decrease in value by percent or increase in value by percent instead of using signs) for the comparison. Please try to give in different lines for different comparisons. Please don't show the comparison of each small component; try to show the comparison of total streams. Please try to show current to previous comparison instead of previous to current.

Now in Asset Management Executive Summary file we have three tables:
  1) Profitability Report ($m)
  2) Flows & Assets Report ($bn)
  3) P&L Report ($m)

The Profitability Report ($m) is linked to P&L Report ($m) as you can see that total revenue in Profitability Report ($m) is the same as P&L Report ($m).
This total revenue in P&L Report ($m) is calculated as: 
       Total Revenue = Total Asset Based Revenue + Perf Fees + Other Dist Fees + Other Rev
So when you do a comparison on total revenue, please do tell because of which component like Mgmt Fee has been increased or decreased there is a change in total revenue by looking at P&L Report ($m). Similarly, try to compare others.

User Question: {user_question}

"Please analyze the Asset Management Executive Summary PDF file and provide commentary on the Profitability Report ($m) and its relation to the P&L Report ($m). Specifically, analyze the Total Revenue in the Profitability Report and compare it to the Total Revenue in the P&L Report for different months, such as Jan 2023 and Feb 2023. Provide insights into any changes, whether increases or decreases, in Total Revenue and explain the main factors contributing to these changes. Please rephrase the commentary after analyzing the file."
   Do this for all the componenets in Profitability Report ($m)
   \n\n{file_contents}\n\nCommentary:"""

    # Call the OpenAI GPT model to generate commentary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides commentary on documents."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": user_question}
        ]
    )

    return response.choices[0].message["content"]

# Initialize Streamlit app
def main():
    st.title("FIL Commentary Generation")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "xlsx", "xls", "csv"])
    user_question = st.text_input("Ask a question based on the generated commentary:")
    
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

        if st.button("Generate Commentary"):
            # Generate commentary using OpenAI GPT model
            commentary = generate_commentary(file_contents, user_question)

            # Display the commentary
            st.subheader("Generated Commentary:")
            st.write(commentary)

if __name__ == "__main__":
    main()
'''


import streamlit as st
import openai
import tempfile
import os
import PyPDF2
import pandas as pd

# Define your OpenAI API key
openai_api_key = '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'

# Function to analyze and generate commentary
def generate_commentary(file_contents, user_question):
    # You can customize the prompt based on your specific use case
    prompt = f"""Please analyze the following document and provide commentary by doing comparison on month on month basis, comparison on Year to date(YTD) basis, comparison on year to year(YTY) basis, and any other combinations possible. Please provide the difference and percentage change (please write decrease in value by percent or increase in value by percent instead of using signs) for the comparison. Please try to give in different lines for different comparisons. Please don't show the comparison of each small component; try to show the comparison of total streams. Please try to show current to previous comparison instead of previous to current.

Now in Asset Management Executive Summary file we have three tables:
  1) Profitability Report ($m)
  2) Flows & Assets Report ($bn)
  3) P&L Report ($m)

The Profitability Report ($m) is linked to P&L Report ($m) as you can see that total revenue in Profitability Report ($m) is the same as P&L Report ($m).
This total revenue in P&L Report ($m) is calculated as: 
       Total Revenue = Total Asset Based Revenue + Perf Fees + Other Dist Fees + Other Rev
So when you do a comparison on total revenue, please do tell because of which component like Mgmt Fee has been increased or decreased there is a change in total revenue by looking at P&L Report ($m). Similarly, try to compare others.

User Question: {user_question}

"Please analyze the Asset Management Executive Summary PDF file and provide commentary on the Profitability Report ($m) and its relation to the P&L Report ($m). Specifically, analyze the Total Revenue in the Profitability Report and compare it to the Total Revenue in the P&L Report for different months, such as Jan 2023 and Feb 2023. Provide insights into any changes, whether increases or decreases, in Total Revenue and explain the main factors contributing to these changes. Please rephrase the commentary after analyzing the file."
   \n\n{file_contents}\n\nCommentary:"""

    # Call the OpenAI GPT model to generate commentary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides commentary on documents."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]

# Initialize Streamlit app
def main():
    st.title("File Analysis and Commentary Generator")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "xlsx", "xls", "csv"])
    user_question = st.text_input("Ask a question based on the generated commentary:")
    
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

        if st.button("Generate Commentary"):
            # Generate commentary using OpenAI GPT model
            commentary = generate_commentary(file_contents, user_question)

            # Display the commentary
            st.subheader("Generated Commentary:")
            st.write(commentary)

if __name__ == "__main__":
    main()

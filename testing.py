from elasticsearch import Elasticsearch
import snowflake.connector
import openai
import streamlit as st

# Snowflake credentials and parameters
snowflake_config = {
    "user": "89abhilash",
    "password": "89@Abhilash",
    "account": "wwwknga-br32220",
    "warehouse": "COMPUTE_WH",
    "database": "FINANCEDWH",
    "schema": "FDWH",
}

def fetch_data_from_snowflake():
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()

    query_table1 = "SELECT * FROM CHANNEL"
    query_table2 = "SELECT * FROM REGION"
    query_table3 = "SELECT * FROM CLIENT"
    query_table4 = "SELECT * FROM FUND"
    query_table5 = "SELECT * FROM FINANCIALS"
    cursor.execute(query_table1)
    data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    st.text(data)
    return data

# Chatbot function
def chatbot(input_text, data):
    relevant_data = []

    for record in data:
        if  record['CHANNEL_NAME'] not in relevant_data:  # Change 'content' to the relevant field
            relevant_data.append(record)

        responses = []
    for record in relevant_data:
        prompt = f"You are a helpful assistant.\nUser: {input_text}\nAssistant: {record['content']}\nUser:"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
    responses.append(response.choices[0].message['content'])
    return responses


def main():
    st.title("SnowChat: Your Snowflake-Powered Chatbot")

    data_from_snowflake = fetch_data_from_snowflake()

    st.text("Data from Snowflake has been loaded. You can now start chatting with the AI Bot!")

    user_input = st.text_area("Send a message")
    if user_input:
        responses = chatbot(user_input, data_from_snowflake)
        st.write("AI Responses:")
        for idx, response in enumerate(responses):
            st.write(f"{idx + 1}. {response}")

if __name__ == "__main__":
    main()


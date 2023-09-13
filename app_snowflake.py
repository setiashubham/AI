from gpt_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import streamlit as st
import tempfile
import snowflake.connector

# Snowflake credentials and parameters
snowflake_config = {
    "user": "89abhilash",
    "password": "89@Abhilash",
    "account": "wwwknga-br32220",
    "warehouse": "COMPUTE_WH",
    "database": "FINANCEDWH",
    "schema": "FDWH",
}

openai_api_key = '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'

def fetch_data_from_snowflake():
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()

    query_table1 = "SELECT * FROM CHANNEL"
    query_table2 = "SELECT * FROM REGION"
    query_table3 = "SELECT * FROM CLIENT"
    query_table4 = "SELECT * FROM FUND"
    query_table5 = "SELECT * FROM FINANCIALS"
	
    
    cursor.execute(query_table1)
    data_table1 = [row for row in cursor.fetchall()]
   # st.table(data_table1)
    
    cursor.execute(query_table2)
    data_table2 = [row for row in cursor.fetchall()]

    cursor.execute(query_table3)
    data_table3 = [row for row in cursor.fetchall()]
    
    cursor.execute(query_table4)
    data_table4 = [row for row in cursor.fetchall()]

    cursor.execute(query_table5)
    data_table5 = [row for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return data_table1 #+data_table2  + data_table3 + data_table4 + data_table5
    #return data_table2



'''def construct_index(data):
    st.text(data)
    #documents = [{"content": item} for item in data]
    st.text('*******')
    #st.text(data)
    index = GPTSimpleVectorIndex(data)
    #index = GPTSimpleVectorIndex(documents)
    index.save_to_disk('index.json')
    return index


def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response
'''

def construct_index(data):
    max_input_size = 4096
    num_outputs = 512
    chunk_overlap_ratio = 0.2
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_overlap_ratio, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = data
    data=[list(i) for i in data]
    st.text(data)
    dic={}
    for i in range(len(data)):
        dic['content'+str(i)]=data[i]
    st.text(dic)
    index = GPTSimpleVectorIndex(dic, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.save_to_disk('index.json')
    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response
def main():
    st.title("Custom-trained AI Chatbot")

    data_from_snowflake = fetch_data_from_snowflake()
    st.text(data_from_snowflake[:10])
    index = construct_index(data_from_snowflake)
    
    st.text("Data from Snowflake has been loaded. You can now start chatting with the AI Bot!")

    user_input = st.text_area("Send a message")
    if user_input:
        response = chatbot(user_input)
        st.text_input("AI Response:")
        st.write(response)

if __name__ == "__main__":
    main()

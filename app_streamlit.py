from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
import openai
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import tempfile

openai_api_key = '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'

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

def main():
    st.title("Custom-trained AI Chatbot")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt"])
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, "uploaded_file.pdf" if uploaded_file.type == "application/pdf" else "uploaded_file.txt"), "wb") as f:
                f.write(uploaded_file.getvalue())

            index = construct_index(tmp_dir)
            st.text("File has been uploaded. You can now start chatting with the AI Bot!")

            user_input = st.text_area("Enter your text:")
            if user_input:
                response = chatbot(user_input)
                st.text_input("AI Response:")
                st.write(response)

if __name__ == "__main__":
    main()
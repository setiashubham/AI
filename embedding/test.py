import requests
import fitz
import re
import shutil
import urllib.request
from pathlib import Path
from tempfile import NamedTemporaryFile
import numpy as np
import tensorflow_hub as hub
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from starlette.middleware.cors import CORSMiddleware
import streamlit as st

# Initialize FastAPI
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SemanticSearch class for text embeddings
class SemanticSearch:
    def __init__(self):
        self.use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i : (i + batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings

recommender = SemanticSearch()

st.title("Financial Report Analysis")
st.sidebar.header("Upload a Text File")

uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt", "pdf"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        # Handle PDF file
        st.sidebar.write("PDF file uploaded")
        # Save the PDF temporarily for processing
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())

        # Provide an option to select pages for processing
        st.sidebar.subheader("Select PDF Pages (Optional)")
        selected_pages = st.sidebar.multiselect(
            "Select the pages to process", list(range(1, fitz.open(temp_pdf.name).page_count + 1))
        )

        # Process selected pages or all pages
        start_page = min(selected_pages) if selected_pages else 1
        end_page = max(selected_pages) if selected_pages else None

        # Extract text from the selected pages
        pdf_text = pdf_to_text(temp_pdf.name, start_page, end_page)
        uploaded_text = "\n".join(pdf_text)

        # Display the extracted text
        st.header("Uploaded PDF Text:")
        st.text(uploaded_text)
    elif uploaded_file.type == "text/plain":
        # Handle plain text file
        st.sidebar.write("Text file uploaded")
        uploaded_text = uploaded_file.read()
        st.header("Uploaded Text:")
        st.text(uploaded_text)

    # Allow the user to ask questions
    st.sidebar.header("Ask a Question:")
    question = st.sidebar.text_input("Ask a question about the text:")

    if st.sidebar.button("Generate Commentary"):
        # Send the text to the FastAPI backend for commentary generation
        payload = {"text": uploaded_text}
        response = requests.post("http://localhost:8000/upload-text-file/", json=payload)
        commentary = response.json()["commentary"]
        st.header("Generated Commentary:")
        st.text(commentary)

    if question:
        if st.sidebar.button("Answer Question"):
            # Send the question to the FastAPI backend for answer generation
            payload = {"question": question}
            response = requests.post("http://localhost:8000/ask-question/", json=payload)
            answer = response.json()["answer"]
            st.header("Generated Answer:")
            st.text(answer)

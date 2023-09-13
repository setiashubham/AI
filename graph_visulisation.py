import streamlit as st
import openai
import plotly.express as px

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app
st.title("GPT-3.5 Turbo Visualization App")

# User input
user_input = st.text_input("Enter your request:")
if user_input:
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=user_input,
        max_tokens=100,
    )
    gpt_response = response.choices[0].text.strip()

    # Display GPT-3.5 Turbo response
    st.write("GPT-3.5 Turbo Response:")
    st.write(gpt_response)

    # Create a sample graph based on the GPT-3.5 Turbo response
    fig = px.line(x=[1, 2, 3, 4, 5], y=[10, 15, 7, 12, 20], title="Sample Graph")

    # Display the graph
    st.plotly_chart(fig)

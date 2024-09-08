import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content,
    extract_body_content
) 
from parse import parse_with_ollama
from parse import parse_with_ollama_test

# Load external Bootstrap CSS
st.markdown(
    """
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <style>
    /* Custom styles */
    body {
        background-color: #000; /* Black background */
        color: #000; /* Black text color */
        margin: 0; /* Remove default margin */
        padding: 20px; /* Add padding for inner content spacing */
        border: 10px solid #ff6f00; /* Orange-yellow border */
        border-radius: 15px; /* Rounded corners */
    }
    .stTextInput>div>input, .stTextArea textarea {
        background-color: #fff; /* White text areas */
        color: #000; /* Black text color */
        border: 1px solid #333; /* Dark border */
        border-radius: 5px; /* Rounded corners */
    }
    .stButton>button {
        background-color: #ff4b4b; /* Red button */
        color: #fff; /* White text */
        border: none; /* Remove default border */
        border-radius: 5px; /* Rounded corners */
    }
    .stButton>button:hover {
        background-color: #e03e3e; /* Darker red on hover */
    }
    .stExpander {
        border: 1px solid #444; /* Dark border for expanders */
        border-radius: 5px; /* Rounded corners */
        background-color: #1c1c1c; /* Dark background for expanders */
    }
    .stExpander>div {
        color: #fff; /* White text inside expanders */
    }
    .container {
        border: 2px solid #333; /* Dark border around the container */
        padding: 20px;
        border-radius: 10px; /* Rounded corners */
    }
    </style>
    """, 
    unsafe_allow_html=True
)


# In main.py, for testing purposes, call the test function
#if st.button("Test Parse"):
#    result = parse_with_ollama_test()
#    st.write(f"Test parse result: {result}")


st.title("AI Web Scrapper")
url = st.text_input("Enter Website Url")

if st.button("Scrape Site"):
    st.write("Scraping the website")
    dom_content = scrape_website(url)
    body_content = extract_body_content(dom_content)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)


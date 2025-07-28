import streamlit as st
from llm_utils import extract_filters
from search_utils import setup_index, semantic_search

st.title("🧪 Semantic Clinical Trial Search")
st.markdown("Enter a natural-language query about trials, and get structured results.")

# Get user input
query = st.text_input("Type your trial search query")

# Get API key (don't store it permanently)
openrouter_api_key = st.text_input("Your OpenRouter API Key", type="password")

if query and openrouter_api_key:
    with st.spinner("Extracting filters via LLM..."):
        filters = extract_filters(query, openrouter_api_key)
        st.subheader("🔍 Extracted Filters")
        st.json(filters)

    with st.spinner("Running semantic search..."):
        df, model, index = setup_index()
        results = semantic_search(filters, df, model, index)

        st.subheader("📋 Matching Trials")
        st.dataframe(results)


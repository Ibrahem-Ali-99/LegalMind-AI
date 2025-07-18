# app.py
import streamlit as st
import torch
from sentence_transformers import SentenceTransformer
from legal_mind_app.config import Config
from legal_mind_app.vector_store import LegalVectorStore
from legal_mind_app.rag_pipeline import RAGPipeline

st.set_page_config(page_title="المحامي الذكي - LegalMind AI", page_icon="⚖️", layout="wide")

@st.cache_resource
def load_embedding_model(_config):
    with st.spinner("Loading embedding model (this happens only once)..."):
        model = SentenceTransformer(_config.EMBEDDING_MODEL, device='cuda' if torch.cuda.is_available() else 'cpu')
    return model

def main():
    st.title("⚖️ المحامي الذكي - LegalMind AI")
    st.caption("Your expert legal assistant for the Egyptian Constitution and Labor Law")

    config = Config()

    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = load_embedding_model(config)
        
    vector_store = LegalVectorStore(config)

    if not vector_store.load():
        st.warning("First-time setup: Vector index not found. Building a new one...")
        vector_store.build_and_save_index(st.session_state.embedding_model)
        vector_store.load() 

    pipeline = RAGPipeline(vector_store, config)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("...اسأل سؤالاً قانونياً"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = pipeline.answer_question(prompt)
            disclaimer = "\n\n---\n*إخلاء مسؤولية: هذه المعلومات للاسترشاد فقط ولا تعد استشارة قانونية. يجب استشارة محامٍ مختص.*"
            full_response = response + disclaimer
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
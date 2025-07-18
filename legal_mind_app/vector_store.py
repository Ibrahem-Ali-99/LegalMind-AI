import pandas as pd
import numpy as np
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from .config import Config

class LegalVectorStore:
    def __init__(self, config: Config):
        self.config = config
        self.index: Optional[faiss.Index] = None
        self.article_records: List[Dict[str, Any]] = []

    def build_and_save_index(self, embedding_model: SentenceTransformer):
        st.write("Building vector index from processed CSV files...")
        
        if not self.config.CONSTITUTION_CSV.exists() or not self.config.LABOR_LAW_CSV.exists():
            st.error(f"Error: One or both source CSV files are missing from '{self.config.INPUT_CSV_DIR}'.")
            st.error("Please run the data processing scripts first.")
            st.stop()
            
        df_c = pd.read_csv(self.config.CONSTITUTION_CSV).assign(source="constitution")
        df_l = pd.read_csv(self.config.LABOR_LAW_CSV).assign(source="labor_law")
        
        df_c = df_c.rename(columns={'arabic_number': 'arabic_number', 'text': 'text'})
        df_l = df_l.rename(columns={'arabic_number': 'arabic_number', 'text': 'text'})

        df_all = pd.concat([df_c[['arabic_number', 'text', 'source']], df_l[['arabic_number', 'text', 'source']]], ignore_index=True)
        df_all.to_csv(self.config.MERGED_DATA_CSV, index=False)
        
        embeddings = embedding_model.encode(df_all["text"].tolist(), show_progress_bar=True, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
        
        faiss.write_index(self.index, str(self.config.FAISS_INDEX_FILE))
        st.success(" Vector index built and saved.")

    def load(self) -> bool:
        if not self.config.FAISS_INDEX_FILE.exists(): return False
        self.index = faiss.read_index(str(self.config.FAISS_INDEX_FILE))
        self.article_records = pd.read_csv(self.config.MERGED_DATA_CSV).to_dict(orient="records")
        return True

    def search(self, q_embedding: np.ndarray, k: int) -> List[Dict[str, Any]]:
        if not self.index: raise RuntimeError("Index not loaded.")
        query = np.array([q_embedding], dtype=np.float32)
        _, indices = self.index.search(query, k)
        return [self.article_records[i] for i in indices[0]]
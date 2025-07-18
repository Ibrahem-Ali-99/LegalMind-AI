from pathlib import Path

class Config:

    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_PATH = PROJECT_ROOT / "data"
    

    INPUT_CSV_DIR = DATA_PATH / "csv"  
    CONSTITUTION_CSV = INPUT_CSV_DIR / "egyptian_constitution.csv" 
    LABOR_LAW_CSV = INPUT_CSV_DIR / "egyptian_labor_law_2025.csv" 


    VECTOR_STORE_PATH = PROJECT_ROOT / "vector_store"
    VECTOR_STORE_PATH.mkdir(exist_ok=True)
    MERGED_DATA_CSV = VECTOR_STORE_PATH / "all_legal_articles.csv"
    FAISS_INDEX_FILE = VECTOR_STORE_PATH / "legal_articles.index"

    EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
    LLM_MODEL = "google/gemma-2-9b-it" 
    
    K_RETRIEVED_DOCS = 5
# ⚖️ LegalMind AI - المحامي الذكي

LegalMind AI is an expert legal assistant powered by Google's Gemma models, designed to provide fast, accurate, and context-aware answers to questions about Egyptian law. It uses a sophisticated Retrieval-Augmented Generation (RAG) pipeline to ensure all responses are grounded in provided legal texts, preventing hallucinations and delivering trustworthy information.

This project is an end-to-end solution, featuring a custom data processing pipeline to ingest legal documents and a user-friendly web interface for interaction.

<img width="1834" height="619" alt="image" src="https://github.com/user-attachments/assets/2ad131b9-9c49-4515-849e-d902204d6bfd" />

## ✨ Features

- **Expert Legal Analysis:** Delivers structured answers including a summary (`الخلاصة`), detailed legal analysis (`التحليل القانوني`), and direct citations (`المواد المُستشهد بها`).
- **Fact-Grounded RAG Pipeline:** All answers are based *exclusively* on the provided legal articles from the Egyptian Constitution and Labor Law to ensure accuracy.
- **Intelligent Abstention:** If the information required to answer a question is not present in the knowledge base, the model will clearly state so in Arabic.
- **High-Performance Inference:** Utilizes the [Groq API](https://groq.com/) for incredibly fast, real-time responses from the powerful `gemma-2-9b-it` model.
- **Interactive UI:** A clean, bilingual chat interface built with Streamlit for an intuitive user experience.
- **Custom Data Ingestion:** A complete, custom-built data pipeline for sourcing and processing legal texts.

---

## ⚙️ Data Collection and Processing

A significant part of this project was building the custom data pipeline to source the legal knowledge base. The data is not pre-packaged; it is collected and processed using the following custom scripts:

1.  **PDF to Text (OCR):** The Egyptian Constitution was sourced from a PDF document. A custom Python script (`scripts/pdf_to_text_ocr.py`) was built using **PyTesseract** and **pdf2image** to perform Optical Character Recognition (OCR), converting the PDF pages into clean, machine-readable text.
2.  **Web Scraping:** The Egyptian Labor Law was sourced from a legal website. A custom Python script (`scripts/scrape_labor_law.py`) was built using **BeautifulSoup** to scrape the article content directly from the web page's HTML.
3.  **Parsing and Cleaning:** A final script (`scripts/parse_articles_from_text.py`) takes the raw text from both sources and uses regular expressions to parse, clean, and structure the data into a final, clean CSV format ready for ingestion.

---

## 🛠️ Tech Stack

- **LLM:** `google/gemma-2-9b-it` via the Groq API
- **Embedding Model:** `intfloat/multilingual-e5-small`
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **Backend & UI:** Streamlit
- **Core Libraries:** Transformers, PyTorch, Sentence-Transformers, Groq, Pandas
- **Data Processing:** pdf2image, PyTesseract, BeautifulSoup, Requests

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.8+
- [Git](https://git-scm.com/downloads)
- **Tesseract OCR Engine:** You must have Tesseract installed on your system. [Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki).
- **Poppler:** Required by `pdf2image` to convert PDFs. [Windows Guide](https://pypi.org/project/pdf2image/).

### 1. Clone the Repository

```bash
git clone https://github.com/Ibrahem-Ali-99/LegalMind-AI.git
cd LegalMind-AI
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

This project requires API keys and paths to local executables.

1.  **Create a `.env` file:** Copy the example file to a new file named `.env`.
    ```bash
    # On Windows
    copy .env.example .env
    # On macOS/Linux
    cp .env.example .env
    ```
2.  **Edit the `.env` file:** Open the new `.env` file and fill in the paths to your local Tesseract and Poppler installations.
3.  **Create a `.streamlit/secrets.toml` file:**
    - In the project's root directory, create a new folder named `.streamlit`.
    - Inside it, create a new file named `secrets.toml`.
    - Add your Groq API key to this file:
      ```toml
      GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
      ```

### 5. Run the Data Pipeline (First-Time Setup)

The application needs structured CSV files as its knowledge base. You must run the data processing scripts in order.

1.  **Place your source PDFs** into the `data/0_source_pdfs/` directory.
2.  **Run the scripts** from the root of the project directory:
    ```bash
    # Run the OCR script for the constitution
    python scripts/1_pdf_to_text_ocr.py

    # Run the web scraper for the labor law
    python scripts/2_scrape_labor_law.py
    
    # Run the final parser script for the constitution text
    python scripts/3_parse_articles_from_text.py
    ```

### 6. Run the Streamlit Application

Once the data pipeline has been run and the `data/2_processed_csv/` directory is populated, you can launch the web app.

```bash
streamlit run app.py
```

Open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

## Future Work

- [ ] Add more legal documents to expand the knowledge base (e.g., Civil Code, Commercial Code).
- [ ] Deploy the application to a cloud service for public access.
- [ ] Improve the parsing script to handle more complex document layouts.

## License

This project is licensed under the MIT License.

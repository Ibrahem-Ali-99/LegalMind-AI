import requests
import streamlit as st
from .config import Config
from .vector_store import LegalVectorStore

class RAGPipeline:
    def __init__(self, vector_store: LegalVectorStore, config: Config):
        self.vector_store = vector_store
        self.config = config
        self.embedding_model = st.session_state.embedding_model
        self.api_url = f"https://api-inference.huggingface.co/models/{self.config.LLM_MODEL}"
        self.headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

    def answer_question(self, question: str) -> str:
        with st.spinner("Searching for relevant legal articles..."):
            q_embedding = self.embedding_model.encode(question)
            matches = self.vector_store.search(q_embedding, k=self.config.K_RETRIEVED_DOCS)
        
        if not matches: return "لم أتمكن من العثور على أي مواد قانونية ذات صلة بالسؤال."
        
        context_text = "\n".join(f"- المصدر: {'قانون العمل' if art['source'] == 'labor_law' else 'الدستور'}, المادة: {art['arabic_number']}\n- النص: {art['text']}" for art in matches)
        
        # --- THIS IS THE CORRECTED, FULLY ARABIC PROMPT ---
        prompt = f"""<start_of_turn>user
أنت مساعد قانوني مصري خبير. مهمتك هي الإجابة على سؤال المستخدم بالاعتماد *الحصري* على السياق القانوني المرفق. اتبع هذه القواعد بصرامة:

1.  **قاعدة القرار:** أولاً، قرر إذا كان "السياق" المرفق يحتوي على معلومات كافية للإجابة بشكل مباشر وواضح على "السؤال".
2.  **قاعدة الامتناع:** إذا كان السياق لا يحتوي على الإجابة، يجب أن تكون استجابتك *فقط* هي هذه الجملة العربية المحددة ولا شيء آخر: `المعلومات المطلوبة غير متوفرة في المواد القانونية المقدمة.`
3.  **قاعدة الإجابة:** إذا كان السياق يحتوي على الإجابة، فيجب أن تلتزم بهذا الهيكل الدقيق بالحرف الواحد:
    `**الخلاصة:**`
    `[ملخص مباشر للإجابة في جملة واحدة]`
    `**التحليل القانوني:**`
    `[شرح مفصل يربط السؤال بالمواد القانونية، مع ذكر أرقام المواد ومصادرها (الدستور أو قانون العمل) بوضوح]`
    `**المواد المُستشهد بها:**`
    `[النص الحرفي الكامل لكل مادة قانونية تم استخدامها في التحليل، مع ذكر رقمها ومصدرها]`

---
### السياق:
{context_text}

### السؤال:
{question}<end_of_turn>
<start_of_turn>model
"""
        with st.spinner("⚖️ المحامي الذكي يفكر (عبر السحابة)..."):
            response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 1024, "return_full_text": False}})
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return "حدث خطأ أثناء الاتصال بالخادم."
            
            api_result = response.json()
            answer = api_result[0]['generated_text'].strip()
        return answer
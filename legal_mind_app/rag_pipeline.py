import streamlit as st
from groq import Groq 
from .config import Config
from .vector_store import LegalVectorStore


class RAGPipeline:
    def __init__(self, vector_store: LegalVectorStore, config: Config):
        self.vector_store = vector_store
        self.config = config
        self.embedding_model = st.session_state.embedding_model
        
        self.groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    def answer_question(self, question: str) -> str:
        with st.spinner("Searching for relevant legal articles..."):
            q_embedding = self.embedding_model.encode(question)
            matches = self.vector_store.search(q_embedding, k=self.config.K_RETRIEVED_DOCS)
        
        if not matches: return "لم أتمكن من العثور على أي مواد قانونية ذات صلة بالسؤال."
        
        context_text = "\n".join(f"- المصدر: {'قانون العمل' if art['source'] == 'labor_law' else 'الدستور'}, المادة: {art['arabic_number']}\n- النص: {art['text']}" for art in matches)
        
        system_prompt = """أنت مساعد قانوني مصري خبير. مهمتك هي الإجابة على سؤال المستخدم بالاعتماد *الحصري* على السياق القانوني المرفق. اتبع هذه القواعد بصرامة:

1.  **قاعدة القرار:** أولاً، قرر إذا كان "السياق" المرفق يحتوي على معلومات كافية للإجابة بشكل مباشر وواضح على "السؤال".
2.  **قاعدة الامتناع:** إذا كان السياق لا يحتوي على الإجابة، يجب أن تكون استجابتك *فقط* هي هذه الجملة العربية المحددة ولا شيء آخر: `المعلومات المطلوبة غير متوفرة في المواد القانونية المقدمة.`
3.  **قاعدة الإجابة:** إذا كان السياق يحتوي على الإجابة، فيجب أن تلتزم بهذا الهيكل الدقيق بالحرف الواحد:
    `**الخلاصة:**`
    `[ملخص مباشر للإجابة في جملة واحدة]`
    `**التحليل القانوني:**`
    `[شرح مفصل يربط السؤال بالمواد القانونية، مع ذكر أرقام المواد ومصادرها (الدستور أو قانون العمل) بوضوح]`
    `**المواد المُستشهد بها:**`
    `[النص الحرفي الكامل لكل مادة قانونية تم استخدامها في التحليل، مع ذكر رقمها ومصدرها]`
"""
        
        user_prompt = f"""---
### السياق:
{context_text}

### السؤال:
{question}
"""
        with st.spinner("⚖️ المحامي الذكي يفكر (عبر Groq API)..."):
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        }
                    ],
                    model="gemma2-9b-it",
                    temperature=0.0, 
                    max_tokens=2048,
                )
                answer = chat_completion.choices[0].message.content
                return answer

            except Exception as e:
                st.error(f"Groq API Error: {e}")
                return "حدث خطأ أثناء الاتصال بخادم Groq."
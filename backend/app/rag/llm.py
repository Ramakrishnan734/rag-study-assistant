from typing import List
from groq import Groq
from app.config.settings import Settings

settings = Settings()
client = Groq(api_key=settings.groq_api_key)


def build_prompt(chunks: List[dict], query: str) -> str:
    context = ""
    for chunk in chunks:
        context += f"Page {chunk['page_number']}: {chunk['text']}\n"
    
    prompt = f"""You are a helpful study assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {query}

Answer:"""
    
    return prompt


def get_answer(chunks: List[dict], query: str) -> str:
    prompt = build_prompt(chunks, query)
    
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
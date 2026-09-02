from typing import List
from groq import Groq
from app.config.settings import Settings

settings = Settings()
client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are an expert study assistant that helps 
students understand their study materials. 
Answer questions clearly and concisely.
Always cite the page number where you found the answer.
If the answer is not in the context, say "I don't know."
Never make up information that is not in the context."""


def build_prompt(chunks: List[dict], query: str) -> str:
    context = ""
    for chunk in chunks:
        context += f"Page {chunk['page_number']}: {chunk['text']}\n"

    user_message = f"""Context:
{context}

Question: {query}

Please provide a clear answer with page citations."""

    return user_message


def get_answer(chunks: List[dict], query: str) -> str:
    prompt = build_prompt(chunks, query)

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
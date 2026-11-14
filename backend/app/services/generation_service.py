
from app.core.groq_client import client


def generate_answer(question, context):

    prompt = f"""
You are an AI assistant that answers questions using
the provided context.

Rules:
1. Answer using only the provided context.
2. Do not invent information.
3. If the answer is not available in the context,
   clearly say that you do not have enough information.
4. Give a clear and understandable answer.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt}],
        temperature=0.2)

    return response.choices[0].message.content

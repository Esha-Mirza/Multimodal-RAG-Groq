
from app.core.groq_client import client

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain Retrieval-Augmented Generation in two simple sentences."
        }
    ],
    temperature=0.3
)

print(response.choices[0].message.content)

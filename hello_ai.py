from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="mistral:7b",  # updated from llama3.2:1b
    messages=[
        {"role": "user", "content": "Explain RAG in one sentence like I am 16."}
    ]
)

print(response.choices[0].message.content)
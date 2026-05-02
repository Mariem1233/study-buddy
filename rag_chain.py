from openai import OpenAI
import chromadb
import PyPDF2

# Step 1: Read PDF
def read_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Step 2: Chunk text
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []
    count = 0

    for word in words:
        current_chunk.append(word)
        count += 1
        if count == chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            count = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Step 3: Store in ChromaDB
def store_chunks(chunks):
    client = chromadb.Client()
    collection = client.create_collection("study_buddy")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )

    return collection

# Step 4: Search ChromaDB
def search(collection, question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    return results["documents"][0]

# Step 5: Generate answer with Mistral
def generate_answer(question, relevant_chunks):
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    context = "\n\n".join(relevant_chunks)

    response = client.chat.completions.create(
        model="mistral:7b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study assistant. Answer questions using ONLY the context provided. If the answer is not in the context, say 'I could not find this in the document.'"
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content

# Run the full RAG chain
print("Loading document...")
text = read_pdf("document.pdf")
chunks = chunk_text(text)
collection = store_chunks(chunks)
print(f"Ready. {len(chunks)} chunks loaded.\n")

# Ask a question
question = input("Ask a question about your document: ")
print("\nSearching document...")
relevant_chunks = search(collection, question)
print("Generating answer...\n")
answer = generate_answer(question, relevant_chunks)
print(f"Answer: {answer}")
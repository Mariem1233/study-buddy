import chromadb
import PyPDF2

# Step 1: Read the PDF
def read_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Step 2: Chunk the text
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

# Step 3: Store chunks in ChromaDB
def store_chunks(chunks):
    client = chromadb.Client()
    collection = client.create_collection("study_buddy")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )

    return collection

# Step 4: Search the collection
def search(collection, question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    return results["documents"][0]

# Run it
text = read_pdf("document.pdf")
chunks = chunk_text(text)
collection = store_chunks(chunks)

print(f"Stored {len(chunks)} chunks in ChromaDB\n")

question = "what is this document about?"
results = search(collection, question)

print(f"Question: {question}\n")
print("Top 3 relevant chunks:")
for i, chunk in enumerate(results):
    print(f"\n--- Result {i+1} ---\n{chunk[:200]}...")

# ChromaDB converted your question into a vector, then found the chunks whose
# vectors were closest in meaning, then returned them.
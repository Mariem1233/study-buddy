import streamlit as st
import chromadb
import PyPDF2
from openai import OpenAI

# ---- Functions ----

def read_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

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

def store_chunks(chunks):
    client = chromadb.Client()
    collection = client.create_collection("study_buddy")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )

    return collection

def search(collection, question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    return results["documents"][0]

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

# ---- UI ----

st.title("📚 Study Buddy")
st.write("Upload any PDF and ask questions about it.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    if "collection" not in st.session_state:
        with st.spinner("Reading and indexing your document..."):
            text = read_pdf(uploaded_file)
            chunks = chunk_text(text)
            st.session_state.collection = store_chunks(chunks)
            st.session_state.chunk_count = len(chunks)

    st.success(f"Ready! {st.session_state.chunk_count} chunks indexed.")

    question = st.text_input("Ask a question about your document:")

    if question:
        with st.spinner("Thinking..."):
            relevant_chunks = search(st.session_state.collection, question)
            answer = generate_answer(question, relevant_chunks)

        st.markdown("### Answer")
        st.write(answer)
import PyPDF2

# Step 1: Read the PDF
def read_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Step 2: Split into chunks
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

    # don't forget the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Run it
text = read_pdf("document.pdf")
chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}")
print(f"\n--- CHUNK 1 ---\n{chunks[0]}")
print(f"\n--- CHUNK 2 ---\n{chunks[1]}")
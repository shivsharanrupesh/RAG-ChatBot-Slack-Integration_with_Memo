import os
import hashlib
import logging
from tqdm import tqdm
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings  # Or OpenAIEmbeddings

logging.basicConfig(
    filename='ingest.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

DATA_DIR           = "data"
VECTOR_STORE_DIR   = "chroma_db"
EMBEDDING_API_KEY  = os.getenv("COHERE_API_KEY")

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def already_embedded(collection, filename, file_hash):
    results = collection.get(where={"filename": filename, "file_hash": file_hash})
    return len(results["ids"]) > 0

def ingest_pdfs(chunk_size=1000, chunk_overlap=200):
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    # 1. set up embeddings + Chroma
    embedding_model = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=EMBEDDING_API_KEY
    )
    vectorstore = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embedding_model
    )

    # 2. configure your splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')]

    for fname in tqdm(pdf_files, desc="Processing PDFs"):
        path = os.path.join(DATA_DIR, fname)
        file_hash = get_file_hash(path)

        # skip if already ingested
        if already_embedded(vectorstore, fname, file_hash):
            logging.info(f"Skipped {fname} (already embedded)")
            continue

        # remove any old chunks for this file
        vectorstore.delete(where={"filename": fname})

        try:
            # 3. load pages
            loader = PyPDFLoader(path)
            pages = loader.load()

            # 4. split each page into smaller chunks
            docs = splitter.split_documents(pages)

            # 5. add to Chroma with metadata
            metadatas = []
            for i, doc in enumerate(docs):
                meta = {
                    "filename": fname,
                    "file_hash": file_hash,
                    # you can include page number if loader provided it:
                    "page": doc.metadata.get("page", None),
                    "chunk_index": i
                }
                metadatas.append(meta)

            vectorstore.add_documents(docs, metadatas=metadatas)
            logging.info(f"Ingested {fname}: {len(docs)} chunks (size={chunk_size}, overlap={chunk_overlap})")

        except Exception as e:
            logging.error(f"Failed to ingest {fname}: {e}")

if __name__ == "__main__":
    ingest_pdfs()
    logging.info("PDF ingestion complete.")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams
import ollama

# 1. Initialize the Embedding Model (runs on local CPU/GPU)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize Qdrant in "Local Mode"
client = QdrantClient(":memory:") # Use a path like "./qdrant_db" to save to disk

def process_and_store(knowledge_base):
    # Create a collection in Qdrant
    client.create_collection(
        collection_name="my_documents",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    # Setup the Chunker
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )

    all_points = []
    
    for doc in knowledge_base:
        chunks = text_splitter.split_text(doc["text"])
        
        for i, chunk_text in enumerate(chunks):
            vector = model.encode(chunk_text).tolist()
            
            point = models.PointStruct(
                id=len(all_points),  # Qdrant needs an integer or UUID
                vector=vector,
                payload={
                    "source": doc["name"],
                    "content": chunk_text
                }
            )
            all_points.append(point)

    client.upsert(
        collection_name="my_documents",
        points=all_points
    )
    print(f"Indexed {len(all_points)} chunks into Qdrant!")
    return client

def search_knowledge(query, limit=3):
    """Finds the most relevant chunks in Qdrant."""
    # 1. Turn the question into a vector
    query_vector = model.encode(query).tolist()
    
    # 2. Search Qdrant
    results = client.query_points(
        collection_name="my_documents",
        query=query_vector,
        limit=limit
    )
    
    # 3. Extract the text content from the results
    relevant_chunks = [hit.payload["content"] for hit in results.points]
    return relevant_chunks
    
def ask_llm(question, context_chunks):
    """Sends context and question to a local model via Ollama."""
    
    # Combine the context chunks
    context_text = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""
    You are a private local assistant. Answer the question using ONLY the context provided.
    If the answer is not in the context, say "I cannot find this in your documents."
    
    CONTEXT:
    {context_text}
    
    USER QUESTION: {question}
    """
    
    # Call the local model
    response = ollama.chat(
        model='qwen2.5:7b',
        messages=[{'role': 'user', 'content': prompt}],
    )
    
    return response['message']['content']
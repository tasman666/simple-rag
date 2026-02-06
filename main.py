import pathlib
from ingestion import process_file
from processing import process_and_store, search_knowledge, ask_llm
from logger_config import chat_logger 

def main():
    source_dir = pathlib.Path("sources")
    if not source_dir.exists(): return

    knowledge_base = []
    for file_path in source_dir.iterdir():
        if file_path.is_file():
            content = process_file(file_path)
            if content:
                knowledge_base.append({"name": file_path.name, "text": content})

    if knowledge_base:
        process_and_store(knowledge_base)
        
        print("\n--- 🤖 RAG Chatbot Ready! ---")
        while True:
            user_query = input("\nAsk a question (or type 'exit'): ")
            if user_query.lower() == 'exit': break
            
            # 1. Get relevant pieces of your files
            context = search_knowledge(user_query)
            
            # 2. Get the AI to summarize them
            answer = ask_llm(user_query, context)

            chat_logger.info(
                f"Interaction for query: {user_query[:30]}...", 
                extra={"details": {
                    "question": user_query,
                    "answer": answer,
                    "context_used": context # Optional: save the sources used
                }}
            )
            
            print(f"\nAI ANSWER:\n{answer}")

if __name__ == "__main__":
    main()
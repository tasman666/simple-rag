import logging
import json
from datetime import datetime

def setup_chat_logger():
    # 1. Create a logger
    logger = logging.getLogger("RAG_Chatbot")
    logger.setLevel(logging.INFO)

    # 2. Create a file handler (saves to 'chat_history.jsonl')
    file_handler = logging.FileHandler("chat_history.jsonl")
    
    # 3. Custom formatter to output JSON
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
            }
            # If we pass extra data (like our question/answer), include it!
            if hasattr(record, "details"):
                log_entry.update(record.details)
            return json.dumps(log_entry)

    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    return logger

# Initialize it once
chat_logger = setup_chat_logger()
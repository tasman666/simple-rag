import pdfplumber
import whisper
import pathlib

def process_file(file_path: pathlib.Path):
    """Determines file type and extracts text."""
    ext = file_path.suffix.lower()
    
    if ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext in [".mp3", ".wav", ".m4a"]:
        return _transcribe_audio(file_path)
    else:
        return None

def _extract_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

def _transcribe_audio(filepath):
    model = whisper.load_model("base")
    result = model.transcribe(str(filepath))
    return result["text"]
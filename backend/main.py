from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pypdf import PdfReader
from llama_cpp import Llama
import tempfile, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
MODEL_PATH = os.path.join(BASE_DIR, "backend", "models", "llama-3.2-1b-instruct-q4_k_m.gguf")

# Create API app
api = FastAPI(title="Local PDF Chatbot API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🦙 Loading model...")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4)
print("✅ Model ready!")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@api.post("/upload")
async def upload_pdf(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)
    with open("context.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return {"message": "PDF uploaded successfully", "text_length": len(text)}

@api.post("/ask")
async def ask_question(question: str = Form(...)):
    if not os.path.exists("context.txt"):
        return JSONResponse({"answer": "Please upload a PDF first."}, status_code=400)

    with open("context.txt", "r", encoding="utf-8") as f:
        context = f.read()

    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    output = llm(prompt, max_tokens=256, stop=["User:", "\n\n"])
    answer = output["choices"][0]["text"].strip()
    return {"answer": answer}


# === Main app to combine API + Frontend ===
from fastapi import FastAPI
app = FastAPI()
app.mount("/api", api)  # all API routes live under /api
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

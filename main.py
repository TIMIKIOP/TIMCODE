from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome bhai, FastAPI chal raha hai 🔥"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/review")
async def review_code(file: UploadFile = File(...)):
    try:
        # Temporary file banake uploaded code save karte hain
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # File ka content AI ko bhejna
        code_text = contents.decode("utf-8")

        # Ollama command call karte hain
        review_prompt = f"Review this code carefully and give suggestions for improvement:\n\n{code_text}"
        result = subprocess.run(
            ["ollama", "run", "codellama", review_prompt],
            capture_output=True,
            text=True
        )

        return {"review": result.stdout.strip()}

    except Exception as e:
        return {"error": str(e)}

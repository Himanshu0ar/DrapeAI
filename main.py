from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import shutil
import os
from tryon_logic import run_tryon

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style='font-family: sans-serif; text-align: center; padding: 50px;'>
        <h1>DrapeAI - Virtual Try-On</h1>
        <form action="/tryon" method="post" enctype="multipart/form-data">
            <p>Person Photo: <input type="file" name="person" required></p>
            <p>Garment Photo: <input type="file" name="garment" required></p>
            <button type="submit">Try It On</button>
        </form>
    </body>
    </html>
    """

@app.post("/tryon")
async def tryon(person: UploadFile = File(...), garment: UploadFile = File(...)):
    person_path = os.path.join(UPLOAD_DIR, "person.jpg")
    garment_path = os.path.join(UPLOAD_DIR, "garment.png")

    with open(person_path, "wb") as f:
        shutil.copyfileobj(person.file, f)
    with open(garment_path, "wb") as f:
        shutil.copyfileobj(garment.file, f)

    output_path = os.path.join(OUTPUT_DIR, "web_result.png")
    success, message = run_tryon(person_path, garment_path, output_path)

    if not success:
        return {"error": message}

    return FileResponse(output_path)

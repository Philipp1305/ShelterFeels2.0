import uvicorn as uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from shelterfeels.database import db
from shelterfeels.voice_recognition_app.config import records_folder, server_port
from shelterfeels.voice_recognition_app.inference_local import extract_key_words_text
from shelterfeels.voice_recognition_app.utils import save_upload_file

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/emotion/{emotion}", response_class=HTMLResponse)
async def emotion_page(emotion: str, request: Request):
    # Map emotion to corresponding HTML file
    emotion_templates = {
        "sad": "sad.html",
        "peaceful": "peaceful.html",
        "powerful": "powerful.html",
        "mad": "mad.html",
        "scared": "scared.html",
        "joyful": "joyful.html",
    }
    template_name = emotion_templates.get(emotion.lower())
    if template_name:
        return templates.TemplateResponse(
            template_name, {"request": request, "emotion": emotion}
        )
    return {"error": "Emotion not found"}


@app.get("/data")
async def get_data():
    data = db.get_data_server()
    if data is None:
        return {"error": "No data found"}
    return {"data": data}


@app.post("/extract_key_words")
def extract_key_words_endpoint(file: UploadFile = File(...)):
    print(file.filename)
    audiofile = save_upload_file(records_folder / file.filename, file)
    print(audiofile)
    keywords = extract_key_words_text(audiofile)
    print("Post processed keywords:", keywords)
    return keywords


@app.get("/liveness_check")
def liveness_check():
    return "good"


if __name__ == "__main__":
    print(f"Service is listening on {server_port}")
    uvicorn.run(app, host="0.0.0.0", port=server_port)

import uvicorn as uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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


@app.get("/emotion/{emotion}")
async def emotion_page(request: Request, emotion: str):
    emotion_styles = {
        "sad": "radial-gradient(ellipse 83.73% 83.73% at 69.09% 34.55%, #6CDFFF 0%, #0011FF 100%), linear-gradient(209deg, #48E1FF 0%, rgba(0, 6.33, 126.52, 0.75) 100%)",
        "peaceful": "radial-gradient(ellipse 83.73% 83.73% at 69.09% 34.55%, #FF00BF 0%, #4B008D 100%), linear-gradient(209deg, #FF48DE 0%, rgba(92.78, 0, 126.52, 0.75) 100%)",
        "powerful": "radial-gradient(ellipse 83.73% 83.73% at 69.09% 34.55%, #03FF10 0%, #006A05 100%), linear-gradient(209deg, #00FF3C 0%, rgba(18.47, 110.83, 0, 0.75) 100%)",
        "mad": "radial-gradient(ellipse 80.20% 80.20% at 67.73% 38.18%, #FF6D5A 0%, #FF0000 100%), linear-gradient(208deg, #FF0000 0%, #FF0000 100%)",
        "scared": "radial-gradient(ellipse 80.20% 80.20% at 67.73% 38.18%, #FFB956 0%, rgba(255, 131.75, 0, 0.49) 100%), linear-gradient(208deg, #FF7700 0%, #FF0000 100%)",
        "joyful": "radial-gradient(ellipse 39.55% 39.55% at 43.64% 46.59%, rgba(255, 248.13, 117.69, 0.49) 0%, #FFB956 100%), linear-gradient(208deg, #FFFB00 0%, #FFA600 100%)",
    }
    style = emotion_styles.get(emotion.lower(), "")
    return templates.TemplateResponse(
        "emotion.html", {"request": request, "emotion": emotion, "style": style}
    )


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

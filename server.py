import uvicorn as uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from shelterfeels.database import db
from shelterfeels.voice_recognition_app.config import records_folder, server_port
from shelterfeels.voice_recognition_app.inference_local import extract_key_words_text
from shelterfeels.voice_recognition_app.utils import save_upload_file


# Ensure the database is set up
app = FastAPI()
db.cache_all_data()  # Preload the cache at startup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def name(request: Request):
    db.cache_all_data()
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/emolearn", response_class=HTMLResponse)
async def emolearn_page(request: Request):
    return templates.TemplateResponse("emolearn.html", {"request": request})


@app.get("/emotion/{emotion}", response_class=HTMLResponse)
async def emotion_page(request: Request, emotion: str):
    # Mapping von Hauptemotion zu Sub-Emotions und Template
    emotion_map = {
        "joyful": {
            "sub_emotions": ("excited", "delightful", "stimulating"),
            "template": "joyful.html",
        },
        "sad": {
            "sub_emotions": ("depressed", "sleepy", "bored"),
            "template": "sad.html",
        },
        "scared": {
            "sub_emotions": ("anxious", "helpless", "insecure"),
            "template": "scared.html",
        },
        "peaceful": {
            "sub_emotions": ("intimate", "loving", "thankful"),
            "template": "peaceful.html",
        },
        "powerful": {
            "sub_emotions": ("confident", "faithful", "appreciated"),
            "template": "powerful.html",
        },
        "mad": {
            "sub_emotions": ("furious", "hurt", "hateful"),
            "template": "mad.html",
        },
    }
    # Check if the emotion is valid
    if emotion not in emotion_map:
        return HTMLResponse(content="Emotion not found", status_code=404)

    # Get the sub-emotions and template for the requested emotion
    sub_emotions = emotion_map[emotion]["sub_emotions"]
    template_name = emotion_map[emotion]["template"]

    # Load cache from JSON file
    cached_data = db.load_cache()  # List of [emotion, word]
    # Filter for relevant emotions
    filtered = [item for item in cached_data if item[0] in sub_emotions]

    # Define positions for the circles
    positions = [
        {"top": "50%", "left": "75%"},
        {"top": "32%", "left": "50%"},
        {"top": "68%", "left": "50%"},
        {"top": "50%", "left": "25%"},
        {"top": "62%", "left": "32%"},
        {"top": "62%", "left": "68%"},
        {"top": "38%", "left": "32%"},
        {"top": "38%", "left": "68%"},
        {"top": "59%", "left": "89%"},
        {"top": "41%", "left": "89%"},
        {"top": "59%", "left": "11%"},
        {"top": "41%", "left": "11%"},
        {"top": "23%", "left": "61%"},
        {"top": "23%", "left": "39%"},
        {"top": "77%", "left": "61%"},
        {"top": "77%", "left": "39%"},
        {"top": "72%", "left": "21%"},
        {"top": "72%", "left": "79%"},
        {"top": "28%", "left": "21%"},
        {"top": "28%", "left": "79%"},
    ]

    # Combine filtered data with positions, fill with "---" if not enough data
    circles = []
    for i, pos in enumerate(positions):
        if i < len(filtered):
            emotion_val, word = filtered[i]
        else:
            emotion_val, word = "---", "---"
        circles.append(
            {
                "emotion": emotion_val,
                "word": word,
                "top": pos["top"],
                "left": pos["left"],
            }
        )

    return templates.TemplateResponse(
        template_name, {"request": request, "circles": circles}
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


@app.get("/emotion-data")
async def emotion_data():
    cached_data = db.load_cache()  # List of [emotion, word]
    # filter for requested emotion
    emotion_groups = {
        "Mad": ["furious", "hurt", "hateful"],
        "Joyful": ["excited", "delightful", "stimulating"],
        "Scared": ["anxious", "helpless", "insecure"],
        "Powerful": ["confident", "faithful", "appreciated"],
        "Peaceful": ["intimate", "loving", "thankful"],
        "Sad": ["depressed", "sleepy", "bored"],
    }

    counts = {}
    for group, sub_emotions in emotion_groups.items():
        counts[group] = sum(1 for entry in cached_data if entry[0] in sub_emotions)

    return counts


@app.get("/liveness_check")
def liveness_check():
    return "good"


if __name__ == "__main__":
    print(f"Service is listening on {server_port}")
    uvicorn.run(app, host="0.0.0.0", port=server_port)

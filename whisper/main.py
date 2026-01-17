from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI(title="Whisper GPU API")

MODEL_ROOT = os.getenv("HF_HOME", "/models")

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16",
    download_root=MODEL_ROOT
)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(
        tmp_path,
        language="pt",
        vad_filter=True,       # remove silêncio
        beam_size=5
    )

    text = " ".join([seg.text for seg in segments])

    os.remove(tmp_path)

    return {
        "language": info.language,
        "duration": info.duration,
        "text": text
    }

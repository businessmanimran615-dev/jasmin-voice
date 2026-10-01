import spaces
from fastapi import FastAPI, Response
import soundfile as sf
import io
from kokoro import KPipeline
import uvicorn

app = FastAPI()

print("Loading Kokoro Pipeline...")
pipeline = KPipeline(lang_code='a')
print("Kokoro Pipeline Loaded Successfully!")

@app.get("/")
def home():
    return {"status": "Jasmin's Voice Server is Alive!"}

@spaces.GPU
@app.get("/speak")
async def speak(text: str):
    try:
        generator = pipeline(
            text, voice='af_bella', 
            speed=1.0, 
            split_pattern=r'\n+'
        )
        
        audio_data = None
        for i, (gs, ps, audio) in enumerate(generator):
            audio_data = audio
            break 
            
        if audio_data is not None:
            buffer = io.BytesIO()
            sf.write(buffer, audio_data, 24000, format='WAV')
            buffer.seek(0)
            return Response(content=buffer.read(), media_type="audio/mpeg")
        else:
            return {"error": "Audio generation failed"}
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
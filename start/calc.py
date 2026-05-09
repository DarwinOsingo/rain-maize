from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

# Pydantic replaces raw dict — FastAPI auto-validates incoming JSON against this
class AskRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5:7b"  # default model, overridable per request

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(data: AskRequest):
    payload = {
        "model": data.model,
        "prompt": data.prompt,
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()  # raises if 4xx/5xx from Ollama
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama unreachable: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
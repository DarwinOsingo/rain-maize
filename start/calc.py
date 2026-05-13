from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
from pydantic import BaseModel
from history import get_session, append_to_session

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

class AskRequest(BaseModel):
    session_id: str
    prompt: str
    model: str = "qwen2.5:1.5b"

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(data: AskRequest):
    history = get_session(data.session_id)
    append_to_session(data.session_id, "user", data.prompt)

    full_prompt = ""
    for message in history:
        full_prompt += f"{message['role']}: {message['content']}\n"
    full_prompt += f"user: {data.prompt}\nassistant:"

    payload = {
        "model": data.model,
        "prompt": full_prompt,
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            ollama_response = response.json()
            reply = ollama_response.get("response", "")
            append_to_session(data.session_id, "assistant", reply)
            return {"reply": reply}
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama unreachable {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
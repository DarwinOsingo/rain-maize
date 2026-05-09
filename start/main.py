from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
from pydantic import BaseModel
app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"
class  AskRequest(BaseModel):
    prompt :str
    model: str = "qwen2.5:1.5b"
@app.get("/health")
async def health():
    return {"status":"ok"}
@app.post("/ask")
async def ask(data:AskRequest):
    payload= {
        "model":data.model,
        "prompt":data.prompt,
        "stream":False
    }
    try:
        async with httpx.AsyncClient(timeout=200) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data.get("response", "")
            return {"reply": reply}
    except httpx.RequestError as e:
       raise HTTPException(status_code=503,detail=f"Ollama unreachable {e}")
    except httpx.HTTPStatusError as e:
       raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")
if __name__== "__main__":
   uvicorn.run(app,host="0.0.0.0",port=8000)
       



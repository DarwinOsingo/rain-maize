from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.post("/ask")
async def ask_ollama(data: dict):

    prompt = data.get("prompt", "")
    model = data.get("model", "qwen2.5:1.5b")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(OLLAMA_URL, json=payload)

        print("STATUS:", response.status_code)
        print("RAW TEXT:", response.text)

        return response.json()

    except Exception as e:
        return {
            "response": f"Backend error: {str(e)}"
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
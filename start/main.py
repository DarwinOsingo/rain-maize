import ollama
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI


class Query(BaseModel):
    prompt : str
    temprature : float = 0.7
@app.post("/ask")
async def ask_quen(query:Query):
    response = ollama.chat(model = 'quen3:4b',
                           messeges = [{'role':'user','content':query.prompt}]
                           
                           )
    return {"response":response['messege']['content']}
    


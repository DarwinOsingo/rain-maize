import requests
import uuid
import httpx
API_URL = "http://127.0.0.1:8000/ask"
session_id = str(uuid.uuid4())

print("="*50)

print(" WELCOME TO THE OLLAMA CLI")
print("="*50)
while True:
   
    user_input = input("Whats your question?: ")
    if user_input in ["exit","quit"]:
        print("Goodbye")
        break
    payload = {
        "session_id":session_id,

        "prompt":user_input
        
    }
    try:
        response = httpx.post(API_URL,json= payload,timeout=300 )
        result= response.json()
        print(f" Assistant:{result.get('reply','No response service unavailable ')}")
    except Exception as e:
        print(f"Error {e}")
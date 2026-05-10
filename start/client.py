import requests
API_URL = "http://127.0.0.1:8000/ask"
print("="*50)

print(" WELCOME TO THE OLLAMA CLI")
print("="*50)
while True:
   
    user_input = input("Whats your question?: ")
    if user_input in ["exit","quit"]:
        print("Goodbye")
        break
    payload = {
        "prompt":user_input
        
    }
    try:
        response = requests.post(API_URL,json= payload)
        result= response.json()
        print(f" Assistant:{result.get('reply','No response service unavailable ')}")
    except Exception as e:
        print(f"Error {e}")
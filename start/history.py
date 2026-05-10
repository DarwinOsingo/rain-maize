import json
import os
HIST_FILE = "history.json"
def load_hist():
    if not os.path.exists(HIST_FILE):
        return{}
    with open(HIST_FILE,"r") as f:
        return json.load(f)
def save_history(data):
    with open(HIST_FILE,"w") as f:
        return json.dump(data,f,indent=2)
def get_sessions(session_id):
    session =load_hist()
    return session.get(session_id,[])
def append_to_session(session_id: str, role: str, content: str):
    sessions = load_hist()                    # load entire file
    if session_id not in sessions:            # first time we've seen this id?
        sessions[session_id] = []             # create a new empty history for it
    sessions[session_id].append({"role": role, "content": content})  # add the message
    save_history(sessions)                    # write the whole thing back to file
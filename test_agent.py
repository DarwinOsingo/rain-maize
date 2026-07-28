import json
import urllib.request

# 1. Define local mock tools (M-Pesa Tax Scenario)
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_kra_tax",
            "description": "Calculates KRA withholding tax (5%) and net payout for local services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "gross_amount": {"type": "number", "description": "Gross amount in KES"},
                    "tax_rate": {"type": "number", "description": "Tax rate decimal, e.g., 0.05 for 5%"}
                },
                "required": ["gross_amount", "tax_rate"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_mpesa_payout",
            "description": "Drafts an M-Pesa B2C payload for reimbursement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "Recipient phone number starting with 254"},
                    "net_amount": {"type": "number", "description": "Net amount to send in KES"}
                },
                "required": ["phone", "net_amount"]
            }
        }
    }
]

# 2. OpenClaw-style Agent Prompt
payload = {
    "model": "qwen2.5:7b",
    "messages": [
        {
            "role": "system",
            "content": "You are a local OpenClaw agent handling Kenyan financial tasks. Use the provided tools to execute multi-step operations."
        },
        {
            "role": "user",
            "content": "Process M-Pesa payment of KES 15,000 for tax consultancy to 254712345678. Calculate 5% withholding tax and draft the net M-Pesa payout."
        }
    ],
    "tools": tools,
    "stream": False
}

print("🤖 Sending multi-step task to local Qwen 2.5 7B via Ollama...\n")

req = urllib.request.Request(
    "http://127.0.0.1:11434/v1/chat/completions",
    data=json.dumps(payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        message = res['choices'][0]['message']
        
        if "tool_calls" in message:
            print("✅ SUCCESS: Qwen generated valid local tool calls:\n")
            print(json.dumps(message["tool_calls"], indent=2))
        else:
            print("💬 Model Response (No direct tool call captured):")
            print(message.get("content"))
except Exception as e:
    print(f"❌ Error connecting to Ollama: {e}")
    print("Ensure Ollama is running (`ollama serve`) and `ollama pull qwen2.5:7b` is complete.")

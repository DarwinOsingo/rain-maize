import json
import urllib.request

# Local Python implementations of your tools
def calculate_kra_tax(gross_amount, tax_rate):
    tax = gross_amount * tax_rate
    net = gross_amount - tax
    return {"status": "success", "gross": gross_amount, "tax_deducted": tax, "net_payout": net}

def draft_mpesa_payout(phone, net_amount):
    return {"status": "queued", "phone": phone, "amount": net_amount, "reference": "TAX-REIMB-001"}

# OpenClaw tool signatures
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_kra_tax",
            "description": "Calculates KRA withholding tax (5%) and net payout for local services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "gross_amount": {"type": "number"},
                    "tax_rate": {"type": "number"}
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
                    "phone": {"type": "string"},
                    "net_amount": {"type": "number"}
                },
                "required": ["phone", "net_amount"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a local OpenClaw agent handling Kenyan financial tasks. Execute all necessary tools step-by-step to complete the request."},
    {"role": "user", "content": "Process M-Pesa payment of KES 15,000 for tax consultancy to 254712345678. Calculate 5% withholding tax first, then draft the net M-Pesa payout."}
]

def query_ollama(msgs):
    payload = {"model": "qwen2.5:7b", "messages": msgs, "tools": tools, "stream": False}
    req = urllib.request.Request(
        "http://127.0.0.1:11434/v1/chat/completions",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))['choices'][0]['message']

# OpenClaw REPL Loop
print("🚀 Starting OpenClaw Multi-Step Execution Loop...\n")

for step in range(1, 5):  # Max 4 turns to prevent infinite loops
    print(f"--- [Turn {step}] Sending context to Qwen 2.5 7B ---")
    msg = query_ollama(messages)
    messages.append(msg)

    # Check if Qwen generated tool calls
    if "tool_calls" in msg and msg["tool_calls"]:
        for tool_call in msg["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            call_id = tool_call.get("id", "call_1")
            
            print(f"🛠️  Qwen requested tool: {func_name}({args})")
            
            # Local tool execution engine
            if func_name == "calculate_kra_tax":
                result = calculate_kra_tax(args["gross_amount"], args["tax_rate"])
            elif func_name == "draft_mpesa_payout":
                result = draft_mpesa_payout(args["phone"], args["net_amount"])
            else:
                result = {"error": "Tool not found"}

            print(f"⚙️  Tool Output: {result}\n")
            
            # Feed tool response back into model memory (OpenAI / OpenClaw standard)
            messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "name": func_name,
                "content": json.dumps(result)
            })
    else:
        print("💬 [FINAL AGENT RESPONSE]:")
        print(msg.get("content"))
        break

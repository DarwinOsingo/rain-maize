import requests
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
response = requests.get(url).text
with open("shakespere.txt","w",encoding = "utf-8") as f:
    f.write(response)
print(f"NUMBER OF CHARCTERS:{len(response)}")
import requests
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
response = requests.get(url).text
print(f"NUMBER OF CHARCTERS:{len(response)}")
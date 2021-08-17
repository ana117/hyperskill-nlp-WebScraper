import requests


def getQuote(target):
    data = requests.get(target).json()

    if "content" not in data:
        return "Invalid quote resource!"
    else:
        return data["content"]


url = input("Input the URL:\n")
print(getQuote(url))

import requests

def fetchAndSaveToFile(url,path):
    r = requests.get(url)
    with open(path,"w") as f:
        f.write(r.text)

url = "https://timesofindia.indiatimes.com/technology"

# r = requests.get(url)
# print(r.text)

fetchAndSaveToFile(url, "harry/data/times.html")
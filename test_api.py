import requests

url = "https://jsearch.p.rapidapi.com/search"

querystring = {
    "query": "python developer remote",
    "page": "1",
    "num_pages": "1"
}

headers = {
    "X-RapidAPI-Key": "d409688413msh0668b78229ce8b4p1cd772jsnf107cc381e2f",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print("Status:", response.status_code)
print("JSON Response:", response.json())
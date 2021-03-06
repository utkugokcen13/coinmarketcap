import requests
import json

api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/"
                           "latest?start=1&limit=5&convert=USD&CMC_"
                           "PRO_API_KEY=0ac7a2fa-1593-4cb0-b0f4-5b15f8889bca")

result = json.loads(api_request.content)
print(result)
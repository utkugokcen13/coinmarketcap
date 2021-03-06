import requests
import json

api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/"
                           "latest?start=1&limit=10&convert=USD&CMC_"
                           "PRO_API_KEY=0ac7a2fa-1593-4cb0-b0f4-5b15f8889bca")

result = json.loads(api_request.content)
#print(result)
#print("Total Count:",result["status"]["total_count"])

sepet = [
    {
        "symbol": "BTC",
        "amount": 3,
        "price": 48000
    },
    {
        "symbol": "ADA",
        "amount": 300,
        "price": 1.05
    },
    {
        "symbol": "LTC",
        "amount": 48,
        "price": 185
    }
]
total_portfolio =0

print("---------------")
for i in range(0,10):
    for coin in sepet:
        if result["data"][i]["symbol"] == coin["symbol"]:
            profit_loss_per_coin = result["data"][i]["quote"]["USD"]["price"] - coin["price"]
            total_profit_loss = profit_loss_per_coin * coin["amount"]
            total_cost = coin["amount"] * coin["price"]
            total_portfolio = total_portfolio + total_profit_loss
            print(result["data"][i]["symbol"] + "-" + result["data"][i]["name"])
            print("Purchase Price: ${0:.2f}".format(coin["price"]))
            print("Amount:",(coin["amount"]))
            print("Current Price: ${0:.2f}".format(result["data"][i]["quote"]["USD"]["price"]))
            print("Total cost: ${0:.2f}".format(total_cost))
            print("Profit / loss per coin: ${0:.2f}".format(profit_loss_per_coin))
            print("Total profit / loss: ${0:.2f}".format(total_profit_loss))


            print("---------------")
print("Total portfolio: ${0:.2f}".format(total_portfolio))

# usecase = "realtime"
usecase = "historical"


crypto_symbols = ["BTC-USD", "ETH-USD", "LTC-USD"]

historical_topics = {
    "BTC-USD": "historical-BTC-USD-topic",
    "ETH-USD": "historical-ETH-USD-topic",
    "LTC-USD": "historical-LTC-USD-topic"
}

realtime_topics = {
    "BTC-USD": "realtime-BTC-USD-topic",
    "ETH-USD": "realtime-ETH-USD-topic",
    "LTC-USD": "realtime-LTC-USD-topic"
}

crypto_names = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "LTC-USD": "Litecoin"
}

crypto_symbol = "BTC-USD"
# crypto_symbol =  "ETH-USD"
# crypto_symbol = "LTC-USD"

historical_topic = historical_topics[crypto_symbol]
realtime_topic = realtime_topics[crypto_symbol]
crypto_name = crypto_names[crypto_symbol]

topic_to_use = historical_topic if usecase == "historical" else realtime_topic
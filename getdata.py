### IMPORTANT: replace first line from resulting CSV file with: i,Date,Open,High,Low,Close,Volume,n,vw


import requests
import pandas as pd

# Set up API key and secret
API_KEY = 'YOUR_KEY'
API_SECRET = 'YOUR_SECRET'

# Set up the request headers with the API key and secret
headers = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': API_SECRET
}

#Choose ticker here
ticker = "JNJ"
start = "2021-01-01"
end = "2023-07-01"

# Make a GET request to the API endpoint
response = requests.get(f'https://data.alpaca.markets/v2/stocks/{ticker}/bars?start=2021-01-01&end=2023-07-01&timeframe=15Min', headers=headers).json()
#Create a dataframe
df = pd.DataFrame(response["bars"])
# Convert the date column to a standard format
df["t"] = pd.to_datetime(df["t"])
# Get next page format
next_page_token = next_page_token = response.get("next_page_token")
while next_page_token:
    response = requests.get(f'https://data.alpaca.markets/v2/stocks/{ticker}/bars?start={start}&end={end}&timeframe=15Min&page_token={next_page_token}', headers=headers).json()
    new_df = pd.DataFrame(response["bars"])
    new_df["t"] = pd.to_datetime(new_df["t"])
    df = df.append(new_df, ignore_index=True)
    next_page_token = response.get("next_page_token")
print(df)
df.to_csv(f"./data/{ticker}.csv")
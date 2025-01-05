from polygon import RESTClient

# Replace with your actual API key
client = RESTClient(api_key="your_api_key")

def test_endpoint(endpoint_name, *args, **kwargs):
    try:
        response = getattr(client, endpoint_name)(*args, **kwargs)
        print(f"Success: {endpoint_name} returned data.")
        print(response)
    except Exception as e:
        print(f"Error: {endpoint_name} is not accessible. {e}")

if __name__ == "__main__":
    test_endpoint("list_aggs", ticker="AAPL", multiplier=1, timespan="day", from_="2022-01-01", to="2022-01-31")
    test_endpoint("get_previous_close", ticker="AAPL")
    test_endpoint("get_ticker_details", ticker="AAPL")
    test_endpoint("get_snapshot_all_tickers")
# fetch_voting_data.py
import requests
import pandas as pd
import json  # for pretty printing JSON

def fetch_voting_data():
    dao_address = "0x1"  # Aptos Governance address (example)
    url = f"https://fullnode.mainnet.aptoslabs.com/v1/accounts/{dao_address}/resources"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Step 1: Print full JSON response structure
        print("Full API response:")
        print(json.dumps(data, indent=2))

        # Step 2: Filter out voting-related entries
        dao_data = [res for res in data if "Voting" in res.get("type", "")]
        if not dao_data:
            print("No DAO voting data found.")
            return pd.DataFrame()

        # Sample field extraction (may need adjustment)
        records = []
        for item in dao_data:
            inner = item.get("data", {})
            records.append({
                "voter": inner.get("voter_address", "N/A"),
                "proposal_id": inner.get("proposal_id", "N/A"),
                "vote": inner.get("vote", "N/A"),
                "timestamp": inner.get("timestamp", 0)
            })

        df = pd.DataFrame(records)
        print("Data has been fetched successfully.")
        return df

    except requests.exceptions.RequestException as e:
        print("Failed to fetch data:", e)
        return pd.DataFrame()

# Run this only when executing the file directly
if _name_ == "_main_":
    df = fetch_voting_data()
    print("\nPreview of fetched data:")
    print(df.head())
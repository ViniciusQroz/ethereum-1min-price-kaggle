import os
import glob
import time
import requests
import pandas as pd
import kaggle


def load_kaggle_dataset(dataset_slug: str) -> pd.DataFrame:
    """
    Download a Kaggle dataset by slug and return it as a pandas DataFrame.
    """
    api = kaggle.api

    temp_path = "temp_download"
    os.makedirs(temp_path, exist_ok=True)

    # Download and unzip the dataset
    api.dataset_download_files(dataset_slug, path=temp_path, unzip=True)

    # Pick the first CSV file
    csv_files = glob.glob(os.path.join(temp_path, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the dataset.")

    return pd.read_csv(csv_files[0])


def fetch_eth_data(pair: str, start_ts: int, end_ts: int, step: int = 60, limit: int = 1000) -> pd.DataFrame:
    """
    Fetch OHLCV data from Bitstamp for a given trading pair between two timestamps.
    """
    url = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/"
    all_candles = []

    while start_ts < end_ts:
        params = {"step": step, "limit": limit, "start": start_ts}
        r = requests.get(url, params=params)
        r.raise_for_status()

        data = r.json()["data"]["ohlc"]
        if not data:
            break

        all_candles.extend(data)

        last_ts = int(data[-1]["timestamp"])
        start_ts = last_ts + step

        time.sleep(1)  # avoid rate limits

    df = pd.DataFrame(all_candles)
    if df.empty:
        return df

    return df.astype({
        "timestamp": "int",
        "open": "float",
        "high": "float",
        "low": "float",
        "close": "float",
        "volume": "float",
    })


def update_kaggle_dataset(dataset_slug: str, folder_path: str, version_notes: str = "Updated dataset"):
    """
    Update an existing Kaggle dataset by replacing old files with new ones.
    """
    api = kaggle.api

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} not found.")

    # Ensure dataset-metadata.json exists
    metadata_path = os.path.join(folder_path, "dataset-metadata.json")
    if not os.path.exists(metadata_path):
        metadata = {
            "title": "Ethereum Historical Data",
            "id": dataset_slug,
            "licenses": [{"name": "CC0-1.0"}]
        }
        import json
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    # Create new version
    api.dataset_create_version(
        folder_path,
        version_notes=version_notes,
        delete_old_versions=True,
        quiet=False
    )

    print(f"Dataset '{dataset_slug}' updated successfully.")



if __name__ == "__main__":
    now_ts = int(time.time())
    pair = "ethusd"
    step = 60
    dataset_slug = "viniciusqroz/ethereum-historical-data"

    # Load most recent data from Kaggle
    df_current = load_kaggle_dataset(dataset_slug)
    latest_unix = int(df_current["timestamp"].max())

    # Fetch new candles
    df_new = fetch_eth_data(
        pair=pair,
        start_ts=latest_unix + step,
        end_ts=now_ts,
        step=step,
    )

    if not df_new.empty:
        updated_df = pd.concat([df_current, df_new], ignore_index=True)

        # Save to temp folder
        upload_dir = "temp_upload"
        os.makedirs(upload_dir, exist_ok=True)

        csv_path = os.path.join(upload_dir, "ethusd_1min_ohlc.csv")
        updated_df.to_csv(csv_path, index=False)

        # Push update to Kaggle
        update_kaggle_dataset(
            dataset_slug=dataset_slug,
            folder_path=upload_dir,
            version_notes=f"Dataset updated on {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    else:
        print("No new data available, nothing to update.")
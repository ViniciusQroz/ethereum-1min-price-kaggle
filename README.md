# Automatic Ethereum Price Update on Kaggle
This project provides an automated pipeline to collect, update, and publish Ethereum (ETH) 1-minute OHLC price data on Kaggle. The dataset is updated daily with the most recent data from the Bitstamp public API and posted automatically to Kaggle.

# Features

Daily Updates: Fetches the latest ETH/USD 1-minute OHLC data and keeps the Kaggle dataset up to date.

Automation with GitHub Actions: The entire update process runs automatically using GitHub Actions.

Easy Deployment: Minimal configuration is required to start updating your Kaggle dataset daily.

# Requirements

Before running the workflow, you need to define two secret variables in your GitHub repository:

API_KEY – Your Bitstamp API key.

KAGGLE_USERNAME – Your Kaggle username (or API token).

# How it Works

The GitHub Actions workflow triggers daily (or manually if needed).

The workflow calls the Bitstamp API to fetch the most recent ETH/USD OHLC data at 1-minute intervals.

The data is saved into a CSV file (ethusd_1min_ohlc.csv).

The workflow uploads the updated dataset to Kaggle automatically using your Kaggle credentials.

# Dataset

The CSV file contains 1-minute interval OHLC Ethereum price data, with Unix timestamps. It is easy to load into Python (pandas), Excel, or any other data analysis tool. The timestamps are consistent, spaced exactly 60 seconds apart, making it suitable for time series analysis and backtesting.

Kaggle link: https://www.kaggle.com/datasets/viniciusqroz/ethereum-historical-data

# Usage

Once the GitHub Actions workflow is configured and the secrets are set, no manual intervention is needed. The dataset on Kaggle will stay up to date automatically.

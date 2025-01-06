![Static Badge](https://img.shields.io/badge/python-%233776ab?logo=python&logoColor=white) ![Static Badge](https://img.shields.io/badge/MIT%20License-grey) ![Static Badge](https://img.shields.io/badge/bitcoin-%23ff9900?logo=bitcoin&logoColor=white)

# **Bitcoin Wallet Fetcher**

**A Python-based tool to automate the fetching, processing, and categorization of Bitcoin wallet addresses from online sources (_Blockchair_)**.<br>This tool **downloads data**, **decompresses it**, and **organizes it into specific categories** for further analysis or usage.

## Table of Contents

- [Project Description](#project-description)
- [Table of Contents](#table-of-contents)
- [What is Bitcoin Wallet Fetcher?](#what-is-bitcoin-wallet-fetcher)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
<!-- - [Usage](#usage)
- [Security and Ethics](#🔐-security-and-ethics)
- [Benchmarks](#benchmarks) -->
- [Roadmap](#roadmap)
- [Tree Directory](#tree-directory)
- [Contributions](#contributions)
- [Support the Project](#support-the-project)
- [License](#license)
- [Author](#author)

## Project Description

**Bitcoin Wallet Fetcher** (_BWF_) is designed to retrieve large datasets of Bitcoin wallet addresses from specified online sources (Blockchair). **It automates downloading, decompressing, and categorizing these addresses into meaningful groupings such as balances, prefix types, and subsets for quick reference or downstream processing.**

## What is Bitcoin Wallet Fetcher?

Bitcoin Wallet Fetcher is a Python script that :

1. Automates file downloads from websites using `Selenium`.
2. Decompresses `.gz` files to extract datasets.
3. Processes Bitcoin wallet addresses and organizes them based on prefixes (`1`, `3`, or `bc1`) and `balance` criteria.
4. Outputs the processed data into structured text files for easier consumption.

## Features

- **Automated File Handling** : Automatically fetch and decompress files.
- **Categorization** : Splits wallet data into categories based on prefix types and balance ranges.
- **Scheduling** : Includes a daily scheduled task to run the entire pipeline at a specified time.
- **Logging** : Provides detailed logs for every step of the process.

## Prerequisites

- `Python 3.11+`
- `Google Chrome` installed
- `ChromeDriver` compatible with your Chrome version
- Environment variables configured in a `.env` file (_see [Installation](#installation)_)
- Required Python libraries (_see [Installation](#installation)_)
  - `selenium`
  - `tqdm`
  - `python-dotenv`

## Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/0x414854/Mnemonic_Hunt.git
   ```

   ```bash
   cd Mnemonic_Hunt

   ```

2. **Run the following command to install libraries**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file with the following structure :**

   ```makefile
   DOWNLOAD_FOLDER = `Path/To/Download/Folder`
   BASE_FILENAME = `blockchair_bitcoin_addresses_latest`
   PROCESSED_FOLDER = `Your/Processed/Folder/Path
   WEBSITE_URL = `https://gz.blockchair.com/bitcoin/addresses/`
   XPATH_FILE = '/html/body/pre/a[2]'
   ```

4. **You're ready to run the program** !

   ```bash
   python3 bitcoinWalletFetcher.py
   ```

## **Roadmap**

- [ ] **Enable sharing of raw and processed files**
- [ ] **Add support for other cryptocurrencies**
  - [ ] **BCH**
  - [ ] **DOGE**
  - [ ] **EGLD**
  - [ ] **ETH**
  - [ ] **LTC**
  - [ ] **SOL**
  - [ ] **XRP**
  - [ ] **ZCASH**
- [ ] **Implement multilingual support for international accessibility**
  - [ ] **French**
  - [ ] **Italian**
  - [ ] **Spanich**
  - [ ] **Portuguese**

## **Tree Directory**

.
<br>├── (.env)
<br>├── .gitignore
<br>├── LICENSE
<br>├── bitcoinWalletFetcher.py
<br>├── (bwf.log)
<br>├── README.md
<br>└── requirements.txt

## **Contributions**

Contributions are welcome ! Feel free to open issues or submit pull requests.

## **Support the Project**

**Giving it a star on GitHub ⭐**

**Your support makes a huge difference !** This project is maintained with the energy, time, and passion of its contributors.
<br>If you enjoy this project or want to help sustain its development, **consider making a donation**.

### 🫶 Why Donate ?

- Help cover development and hardware costs.
- Contribute to new features and improvements.
- Support an open-source project to keep it free and accessible to everyone.

### 🪙 Cryptocurrency Wallets

You can donate using the following cryptocurrency addresses:

- **Bitcoin (BTC)** : `bc1q6n3ufauzjqgxztkklj3734cp0f7evqq3djh4ne`
- **Ethereum (ETH)** : `0x24800123e8D51F1d596c6Abe4B5DB5A10837Fe8e`
- **Bittensor (TAO)** : `5CrG7bKratZVocnxj66FF23AMVvqKHf7RSHfz49csEtJ2CuG`
- **Dogecoin (DOGE)** : `DJQnasX39Unat3vkmyBMgp4H6Kfd4wFumF`
- **Solana (SOL)** : `Gj9JkpFqdSabag8RiiNTmLaCiZrcxYa6pc4y599vft15`

#### **USDT (Tether)**

- **Binance Smart Chain (BEP-20)** : `0x24800123e8D51F1d596c6Abe4B5DB5A10837Fe8e`
- **Ethereum (ERC-20)** : `0x24800123e8D51F1d596c6Abe4B5DB5A10837Fe8e`
- **Tron (TRC-20)** : `THHcEQ8zG3ZnUXoHdBmCdpZ3AAqhoDbMpW`
- **Solana (SPL)** : `Gj9JkpFqdSabag8RiiNTmLaCiZrcxYa6pc4y599vft15`

#### **USDC (USD Coin)**

- **Binance Smart Chain (BEP-20)**: `0x24800123e8D51F1d596c6Abe4B5DB5A10837Fe8e`
- **Ethereum (ERC-20)**: `0x24800123e8D51F1d596c6Abe4B5DB5A10837Fe8e`
- **Solana (SPL)**: `Gj9JkpFqdSabag8RiiNTmLaCiZrcxYa6pc4y599vft15`

### 💬 A Big Thank You

Thank you so much for your generosity. Your support truly means the world to us and motivates us to keep improving this project. 🙏

**➡️ Take action now ! Every contribution, big or small, makes a huge impact.**

## **License**

This project is licensed under the **[MIT License](https://github.com/0x414854/Satoshi_Hunter/blob/main/LICENSE)**.

## **Author**

[**0x414854**](https://github.com/0x414854)

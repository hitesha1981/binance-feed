# Binance WebSocket Feed

Author: Hitesh Agrawal

A simple Python implementation for consuming **Binance Spot Testnet WebSocket feeds**, listening to:

- **Trade streams** (`@trade`)
- **BookTicker streams** (`@bookTicker`)

This project is intended for learning, testing, and prototyping against Binance Testnet using **Ed25519 API key authentication**.

---

## 📋 Overview

This project connects to the Binance WebSocket API and streams real-time market data, including:

- Executed trades (price, quantity, timestamp)
- Best bid/ask prices with quantities (order book top)

It uses Binance **Spot Testnet**, making it safe for experimentation without real funds.

---

## ✨ Features

- Real-time WebSocket connection to Binance Testnet
- Supports multiple streams (trade + bookTicker)
- Uses **Ed25519 API keys** (recommended by Binance)
- Configurable trading symbol
- Lightweight and easy to extend

---

## 🧰 Tech Stack

- Python 3.7+
- WebSocket client
- Binance Spot Testnet
- OpenSSL (for key generation)

---

## 🚀 Quick Start

### Prerequisites

- Python **3.7 or newer**
- `openssl` installed
- Binance Spot **Testnet account**
- GitHub account (required by Binance Testnet)

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd binance-feed
```

---

### 2️⃣ Create a `.env` file

```env
BINANCE_TESTNET_API_KEY="your_ed25519_api_key_here"
SYMBOL="btcusdt"
WS_URL="wss://stream.testnet.binance.vision/stream"
```

---

## 🔐 Generating an Ed25519 API Key (Binance Testnet)

### Step 1: Create a Testnet account
https://testnet.binance.vision/

### Step 2: Generate a private key
```bash
openssl genpkey -algorithm ed25519 -out test-prv-key.pem
```

### Step 3: Generate the public key
```bash
openssl pkey -pubout -in test-prv-key.pem -out test-pub-key.pem
```

### Step 4: Register the public key
https://testnet.binance.vision/key/register

---

## ▶️ Running the Application
```bash
python main.py
```

---

## ▶️ Test Output
```bash
✅ Connected to BTCUSDT
[0001] bookTicker    | BID:$89639.52000000 ASK:$89639.53000000
[0002] trade        ⏱️ -63.0ms | $89639.53000000×0.02228000 BUY ID:4660536
[0003] bookTicker    | BID:$89639.52000000 ASK:$89639.53000000
[0004] trade        ⏱️ -62.3ms | $89639.53000000×0.00111000 BUY ID:4660537
[0005] bookTicker    | BID:$89639.52000000 ASK:$89639.53000000
[0006] trade        ⏱️ -60.6ms | $89639.53000000×0.02228000 BUY ID:4660538
[0007] bookTicker    | BID:$89646.28000000 ASK:$89652.78000000
[0008] bookTicker    | BID:$89646.28000000 ASK:$89646.29000000
[0009] trade        ⏱️ -63.9ms | $89646.28000000×0.00100000 SELL ID:4660539
[0010] bookTicker    | BID:$89646.28000000 ASK:$89646.29000000
[0011] trade        ⏱️ -64.1ms | $89646.28000000×0.00111000 SELL ID:4660540
[0012] bookTicker    | BID:$89646.28000000 ASK:$89646.29000000
[0013] trade        ⏱️ -63.8ms | $89646.29000000×0.00111000 BUY ID:4660541
[0014] bookTicker    | BID:$89646.28000000 ASK:$89646.29000000
^C
📊 Final: 14 messages
```

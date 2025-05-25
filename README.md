# 🧠 LLM Dataset Approval with DAO + Blockchain

This project implements a prototype system for decentralized dataset governance in LLM (Large Language Model) training using Ethereum smart contracts and DAO-based approval workflows. It ensures that only transparent and verifiable datasets are included for LLM training by verifying their integrity on-chain using SHA256 hashes.

## ✨ Features

- 🗃️ Dataset proposal with metadata (CSV + JSON)
- 🔐 Smart contract on Sepolia testnet to log and approve datasets
- ✅ GUI tools to propose, approve, and verify dataset hashes
- 📦 Uses SHA256 to bind dataset files and validate integrity
- 🧑‍💻 Built using Python, Web3.py, Tkinter, and Solidity

---

## 📁 Project Structure
```
LLM-DAO-traceability/
├── smart_contract/
│ ├── contracts/
│ │ └── DataApprovalDAO.sol
│ ├── scripts/
│ │ └── deploy.js
│ ├── contract_info.json # Deployed contract address
│ ├── contract_abi.json # ABI for use in Python GUIs
│ └── hardhat.config.js
├── showcase/
│ ├── gui_propose.py # Propose new dataset
│ ├── gui_approve.py # Approve proposed datasets
│ ├── gui_verify_csv.py # Verify dataset status on-chain
│ └── requirements.txt
├── dataset/
│ ├── sample.csv
│ ├── sample_metadata.json
│ └── ...
└── .env # Contains private key and RPC settings

```

---

## 🚀 Quick Start

### 1. Clone the repository and install dependencies

```bash
cd LLM-DAO-traceability/showcase
pip install -r requirements.txt
```
### 2. Prepare .env in the root or showcase/ folder
```
PRIVATE_KEY=your_private_key_here
ACCOUNT_ADDRESS=0xYourWalletAddress
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your_api_key
```
💡 Make sure your MetaMask wallet has Sepolia testnet ETH!


### 🧪 Run the GUIs
```bash
# Propose a dataset
python showcase/gui_propose.py

# Approve datasets (for owner)
python showcase/gui_approve.py

# Verify all CSVs in dataset/
python showcase/gui_verify_csv.py
```

(the verifying csv should be in dataset directory)
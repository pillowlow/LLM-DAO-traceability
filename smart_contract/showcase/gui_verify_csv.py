import os
import json
import hashlib
import tkinter as tk
from tkinter import ttk
from web3 import Web3
from dotenv import load_dotenv

# === Load Environment ===
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = Web3.to_checksum_address(os.getenv("ACCOUNT_ADDRESS"))
SEPOLIA_URL = os.getenv("SEPOLIA_RPC_URL")

with open("contract_info.json", "r") as f:
    CONTRACT_ADDRESS = json.load(f)["contract_address"]

with open("contract_abi.json", "r") as f:
    CONTRACT_ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider(SEPOLIA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

DATASET_DIR = "..\..\dataset"

# === Helper Functions ===
def hash_csv(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_all_csv_status():
    tree.delete(*tree.get_children())
    for file in os.listdir(DATASET_DIR):
        if file.endswith(".csv"):
            csv_path = os.path.join(DATASET_DIR, file)
            cid = hash_csv(csv_path)
            try:
                proposal = contract.functions.proposals(cid).call()
                proposer = proposal[1]
                approved = proposal[2]
            except Exception:
                proposer = "N/A"
                approved = False
            tree.insert("", "end", values=(file, cid, approved, proposer))

# === GUI Setup ===
root = tk.Tk()
root.title("CSV Dataset Chain Verifier")
root.geometry("960x400")

tk.Button(root, text="Refresh CSV Status", command=load_all_csv_status).pack(pady=5)

columns = ("CSV File", "CID", "Approved", "Proposer")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250 if col == "CID" else 150)
tree.pack()

load_all_csv_status()
root.mainloop()

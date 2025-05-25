import os
import json
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk
from web3 import Web3
from dotenv import load_dotenv

# === Setup ===
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

DATASET_DIR = "..\dataset"

# === Helper Functions ===
def hash_csv(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def find_csv_by_cid(cid):
    for file in os.listdir(DATASET_DIR):
        if file.endswith(".csv"):
            if hash_csv(os.path.join(DATASET_DIR, file)) == cid:
                return os.path.join(DATASET_DIR, file)
    return None

def approve_cid(cid):
    try:
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn = contract.functions.approveDataset(cid).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        messagebox.showinfo("Success", f"Approved CID:\n{cid}\nTx: {tx_receipt.transactionHash.hex()}")
        load_proposed_cids()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_proposed_cids():
    tree.delete(*tree.get_children())
    for file in os.listdir(DATASET_DIR):
        if file.endswith(".csv"):
            csv_path = os.path.join(DATASET_DIR, file)
            cid = hash_csv(csv_path)
            approved = contract.functions.isApproved(cid).call()
            if not approved:
                json_path = csv_path.replace(".csv", "_metadata.json")
                if os.path.exists(json_path):
                    with open(json_path) as f:
                        meta = json.load(f)
                    tree.insert("", "end", values=(file, meta.get("author", ""), meta.get("task", ""), cid))

def handle_approve():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a row to approve.")
        return
    cid = tree.item(selected[0], "values")[3]
    approve_cid(cid)

# === GUI ===
root = tk.Tk()
root.title("Simulated Cloud Dataset Approval")
root.geometry("880x400")

tk.Button(root, text="Reload Proposed CIDs", command=load_proposed_cids).pack(pady=5)
tk.Button(root, text="Approve Selected", command=handle_approve, bg="#4CAF50", fg="white").pack(pady=5)

columns = ("CSV File", "Author", "Task", "CID")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "CID" else 400)
tree.pack()

load_proposed_cids()
root.mainloop()

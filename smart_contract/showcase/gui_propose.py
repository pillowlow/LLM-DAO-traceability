import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
import hashlib
import json
import os
from web3 import Web3
from dotenv import load_dotenv

# === Load .env Variables ===
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = Web3.to_checksum_address(os.getenv("ACCOUNT_ADDRESS"))
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")

# === Load Contract Info ===
with open("contract_info.json", "r") as f:
    contract_address = json.load(f)["contract_address"]

with open("contract_abi.json", "r") as f:
    contract_abi = json.load(f)

# === Connect to Web3 ===
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# === GUI Logic ===
def drop(event):
    file_entry.delete(0, tk.END)
    file_entry.insert(0, event.data.strip('{}'))

def propose_dataset():
    filepath = file_entry.get().strip()
    author = entry_author.get().strip()
    task = entry_task.get().strip()
    license_type = entry_license.get().strip() or "CC-BY 4.0"
    description = text_description.get("1.0", "end-1c").strip()

    if not filepath or not os.path.isfile(filepath):
        messagebox.showerror("Error", "Please select a valid CSV file.")
        return
    if not author or not task:
        messagebox.showerror("Error", "Author and Task are required.")
        return

    with open(filepath, 'rb') as f:
        file_data = f.read()
        cid = hashlib.sha256(file_data).hexdigest()

    metadata = {
        "author": author,
        "task": task,
        "license": license_type,
        "description": description,
        "sha256": cid
    }

    meta_output = os.path.splitext(filepath)[0] + "_metadata.json"
    with open(meta_output, "w") as f:
        json.dump(metadata, f, indent=4)

    try:
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn = contract.functions.proposeDataset(cid).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        messagebox.showinfo("Success", f"Proposed CID on-chain!\nCID: {cid}\nTx: {tx_receipt.transactionHash.hex()}\nMetadata saved to:\n{meta_output}")
    except Exception as e:
        messagebox.showerror("Error", f"Blockchain transaction failed:\n{e}")

# === GUI Setup ===
root = TkinterDnD.Tk()
root.title("LLM DAO Dataset Proposer with Metadata")
root.geometry("650x500")

tk.Label(root, text="Drag CSV file here or click below to browse:", font=("Arial", 12)).pack(pady=10)
file_entry = tk.Entry(root, width=60)
file_entry.pack()
file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', drop)

tk.Label(root, text="Author *", font=("Arial", 12)).pack()
entry_author = tk.Entry(root, width=60)
entry_author.pack()

tk.Label(root, text="Task *", font=("Arial", 12)).pack()
entry_task = tk.Entry(root, width=60)
entry_task.pack()

tk.Label(root, text="License (default: CC-BY 4.0)", font=("Arial", 12)).pack()
entry_license = tk.Entry(root, width=60)
entry_license.insert(0, "CC-BY 4.0")
entry_license.pack()

tk.Label(root, text="Description", font=("Arial", 12)).pack()
text_description = tk.Text(root, height=4, width=60)
text_description.pack()

tk.Button(root, text="Propose Dataset", command=propose_dataset, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=15)

root.mainloop()
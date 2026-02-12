from algosdk.v2client import algod
from algosdk import transaction
import json

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# Load your Python wallet
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

ASSET_ID = 10458941

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Check if already opted in
account_info = algod_client.account_info(student_address)
asset_opted_in = False
for asset in account_info.get('assets', []):
    if asset['asset-id'] == ASSET_ID:
        asset_opted_in = True
        balance = asset['amount']
        print(f"✅ Already opted in! Balance: {balance / 100} INR")
        break

if not asset_opted_in:
    # Opt in to the asset
    params = algod_client.suggested_params()
    
    optin_txn = transaction.AssetTransferTxn(
        sender=student_address,
        sp=params,
        receiver=student_address,  # Opt-in by sending to yourself
        amt=0,
        index=ASSET_ID
    )
    
    signed_optin = optin_txn.sign(PRIVATE_KEY)
    txid = algod_client.send_transaction(signed_optin)
    transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"✅ Successfully opted into asset {ASSET_ID}")
    print(f"Transaction: https://testnet.algoexplorer.io/tx/{txid}")

print("\n🎉 You can now receive and send this asset!")
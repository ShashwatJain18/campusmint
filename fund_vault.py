from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import PaymentTxn, AssetTransferTxn, wait_for_confirmation
import json

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# ===== LOAD PYTHON WALLET =====
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

# ===== YOUR DEPLOYED VAULT =====
APP_ID = 755414328
APP_ADDRESS = "XNYOP7SKZTKZPFTFUV5PNOQVBSKADARFSBYJ2KRB42H4YEACGUGOTU5ET4"
ASSET_ID = 10458941

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

print("=" * 50)
print("💰 FUNDING VAULT CONTRACT")
print("=" * 50)

# Step 1: Fund app with 1 ALGO for fees
params = algod_client.suggested_params()
fund_txn = PaymentTxn(
    sender=student_address,
    sp=params,
    receiver=APP_ADDRESS,
    amt=1_000_000  # 1 ALGO
)
signed_fund = fund_txn.sign(PRIVATE_KEY)
txid = algod_client.send_transaction(signed_fund)
wait_for_confirmation(algod_client, txid, 4)
print(f"✅ Vault funded with 1 ALGO")

# Step 2: Check if vault already opted into asset
app_account_info = algod_client.account_info(APP_ADDRESS)
asset_opted_in = False
for asset in app_account_info.get('assets', []):
    if asset['asset-id'] == ASSET_ID:
        asset_opted_in = True
        break

if not asset_opted_in:
    # Need to opt-in the vault to the asset
    print("⚠️ Vault not opted into asset. You need to opt-in first.")
    print("\nRun this command to opt-in:")
    print("\n```python")
    print("from algosdk.v2client import algod")
    print("from algosdk import transaction")
    print("import json")
    print("\nalgod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')")
    print("with open('python_wallet.json', 'r') as f:")
    print("    wallet = json.load(f)")
    print("PRIVATE_KEY = wallet['private_key']")
    print("student_address = wallet['address']")
    print("APP_ADDRESS = 'XNYOP7SKZTKZPFTFUV5PNOQVBSKADARFSBYJ2KRB42H4YEACGUGOTU5ET4'")
    print("ASSET_ID = 10458941")
    print("\nparams = algod_client.suggested_params()")
    print("optin_txn = transaction.AssetTransferTxn(")
    print("    sender=student_address,")
    print("    sp=params,")
    print("    receiver=APP_ADDRESS,")
    print("    amt=0,")
    print("    index=ASSET_ID")
    print(")")
    print("signed_optin = optin_txn.sign(PRIVATE_KEY)")
    print("txid = algod_client.send_transaction(signed_optin)")
    print("transaction.wait_for_confirmation(algod_client, txid, 4)")
    print("print('✅ Vault opted into asset')")
    print("```")
else:
    print("✅ Vault already opted into asset")

print("\n" + "=" * 50)
print("✅ SETUP COMPLETE")
print("=" * 50)
print(f"\n📊 Vault Address: {APP_ADDRESS}")
print(f"📊 Asset ID: {ASSET_ID}")
print(f"📊 Your Address: {student_address}")
from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationCallTxn, wait_for_confirmation
import json
import base64

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# Load wallet
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

# This vault is already unlocked (755414948)
APP_ID = 755414948
APP_ADDRESS = "335NRKCB2ZCL4OA56CIEAYV2PKQ7ZDOII3ZBVRX7QKWUGUI2232WN4N2BY"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

print("=" * 50)
print("🔓 ATTEMPTING WITHDRAWAL FROM UNLOCKED VAULT")
print("=" * 50)

# Check if vault has funds
app_info = algod_client.application_info(APP_ID)
amount = 0
for item in app_info['params']['global-state']:
    key = base64.b64decode(item['key']).decode('utf-8')
    if key == 'amount':
        amount = item['value']['uint']
        print(f"💰 Vault balance: {amount / 1_000_000} ALGO")

if amount == 0:
    print("❌ Vault is empty - nothing to withdraw")
    exit()

# Withdraw
params = algod_client.suggested_params()
app_call = ApplicationCallTxn(
    sender=student_address,
    sp=params,
    index=APP_ID,
    on_complete=transaction.OnComplete.NoOpOC,
    app_args=["withdraw"]
)

signed = app_call.sign(PRIVATE_KEY)
txid = algod_client.send_transaction(signed)
wait_for_confirmation(algod_client, txid, 4)

print(f"✅ WITHDRAWAL SUCCESSFUL!")
print(f"Transaction: https://testnet.algoexplorer.io/tx/{txid}")
from algosdk.v2client import algod
from algosdk import transaction
import json

algod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')
with open('python_wallet.json', 'r') as f:
    wallet = json.load(f)
PRIVATE_KEY = wallet['private_key']
student_address = wallet['address']
APP_ADDRESS = 'XNYOP7SKZTKZPFTFUV5PNOQVBSKADARFSBYJ2KRB42H4YEACGUGOTU5ET4'
ASSET_ID = 10458941

params = algod_client.suggested_params()
optin_txn = transaction.AssetTransferTxn(
    sender=student_address,
    sp=params,
    receiver=APP_ADDRESS,
    amt=0,
    index=ASSET_ID
)
signed_optin = optin_txn.sign(PRIVATE_KEY)
txid = algod_client.send_transaction(signed_optin)
transaction.wait_for_confirmation(algod_client, txid, 4)
print('✅ Vault opted into asset')
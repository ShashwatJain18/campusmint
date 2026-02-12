from algosdk.v2client import algod
import json

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# Your Python wallet address
PYTHON_ADDRESS = "7TU3QENSSVW3JZPWMSVHLYRDOIVWYBDJBF4YV5FB6WLLQICPWCGTJTSDWM"

# Create client
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Get account info
account_info = algod_client.account_info(PYTHON_ADDRESS)
balance = account_info['amount'] / 1_000_000  # Convert from microALGO to ALGO

print(f"Python Wallet Address: {PYTHON_ADDRESS}")
print(f"Balance: {balance} ALGO")
print(f"Full account info: {json.dumps(account_info, indent=2)}")
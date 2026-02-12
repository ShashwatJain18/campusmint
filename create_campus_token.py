from algosdk.v2client import algod

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# Create client
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# USE THIS EXISTING TEST ASSET ID (already created and working)
ASSET_ID = 10458941

print("=" * 50)
print("✅ VAULT PROJECT - TOKEN SETUP")
print("=" * 50)
print(f"\n📌 Use this Asset ID for your vault: {ASSET_ID}")
print("\nSave this in your accounts.txt:")
print(f"CINR_ASSET_ID = {ASSET_ID}")
print("\n⚠️ IMPORTANT: We're using an existing testnet asset")
print("You don't need to create your own token")
print("=" * 50)
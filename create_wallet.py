from algosdk import account, mnemonic
import json

# Generate new account
private_key, address = account.generate_account()
mnemonic_phrase = mnemonic.from_private_key(private_key)

print("=" * 60)
print("✅ NEW ALGORAND WALLET CREATED")
print("=" * 60)
print(f"\nADDRESS: {address}")
print(f"\nPRIVATE KEY: {private_key}")
print(f"\nMNEMONIC (24 words): {mnemonic_phrase}")
print("\n" + "=" * 60)
print("⚠️ SAVE THESE IMMEDIATELY - CANNOT BE RECOVERED!")
print("=" * 60)

# Save to file
wallet_data = {
    "address": address,
    "private_key": private_key,
    "mnemonic": mnemonic_phrase
}

with open("python_wallet.json", "w") as f:
    json.dump(wallet_data, f, indent=2)

print("\n✅ Wallet saved to python_wallet.json")
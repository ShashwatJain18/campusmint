from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationCallTxn, PaymentTxn, wait_for_confirmation
import base64
import json
import time

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# ===== LOAD PYTHON WALLET =====
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

# ===== YOUR NEW 1-MINUTE VAULT =====
APP_ID = 755414948
APP_ADDRESS = "335NRKCB2ZCL4OA56CIEAYV2PKQ7ZDOII3ZBVRX7QKWUGUI2232WN4N2BY"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def check_vault_state():
    print("\n" + "=" * 50)
    print("📊 VAULT STATE")
    print("=" * 50)
    
    app_info = algod_client.application_info(APP_ID)
    global_state = app_info['params']['global-state']
    
    for item in global_state:
        key = base64.b64decode(item['key']).decode('utf-8')
        value = item['value']
        
        if value['type'] == 1:
            if key == "beneficiary":
                addr_bytes = base64.b64decode(value['bytes'])
                addr = addr_bytes.decode('utf-8')
                print(f"  {key}: {addr}")
            else:
                print(f"  {key}: (set)")
        else:
            if key == "amount":
                print(f"  {key}: {value['uint'] / 1_000_000} ALGO")
            elif key == "unlock_time":
                unlock = value['uint']
                now = int(time.time())
                if now < unlock:
                    seconds = unlock - now
                    print(f"  {key}: {unlock} (🔒 LOCKED - {seconds} seconds remaining)")
                else:
                    print(f"  {key}: {unlock} (🔓 UNLOCKED)")

def deposit_to_vault(amount_algo):
    print("\n" + "=" * 50)
    print(f"💰 DEPOSITING {amount_algo} ALGO TO VAULT")
    print("=" * 50)
    
    amount_micro = int(amount_algo * 1_000_000)
    params = algod_client.suggested_params()
    
    app_call = ApplicationCallTxn(
        sender=student_address,
        sp=params,
        index=APP_ID,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=["deposit"]
    )
    
    payment = PaymentTxn(
        sender=student_address,
        sp=params,
        receiver=APP_ADDRESS,
        amt=amount_micro
    )
    
    gid = transaction.calculate_group_id([app_call, payment])
    app_call.group = gid
    payment.group = gid
    
    signed_app_call = app_call.sign(PRIVATE_KEY)
    signed_payment = payment.sign(PRIVATE_KEY)
    
    txid = algod_client.send_transactions([signed_app_call, signed_payment])
    wait_for_confirmation(algod_client, txid, 4)
    
    print(f"✅ Deposited {amount_algo} ALGO!")
    print(f"Transaction: https://testnet.algoexplorer.io/tx/{txid}")

def try_withdraw():
    print("\n" + "=" * 50)
    print("🔓 ATTEMPTING WITHDRAWAL")
    print("=" * 50)
    
    params = algod_client.suggested_params()
    
    app_call = ApplicationCallTxn(
        sender=student_address,
        sp=params,
        index=APP_ID,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=["withdraw"]
    )
    
    signed = app_call.sign(PRIVATE_KEY)
    
    try:
        txid = algod_client.send_transaction(signed)
        wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ WITHDRAWAL SUCCESSFUL!")
        print(f"Transaction: https://testnet.algoexplorer.io/tx/{txid}")
        return True
    except Exception as e:
        print(f"❌ REJECTED: Time lock not reached yet!")
        return False

# ===== DEMO =====
print("\n" + "🎓" * 25)
print("🎓 1-MINUTE TIME-LOCKED VAULT DEMO")
print("🎓" * 25)

# Check initial state
check_vault_state()

# Deposit 5 ALGO
deposit_to_vault(5)

# Check state after deposit
check_vault_state()

# Try immediate withdrawal (should fail)
print("\n⏰ Trying immediate withdrawal (should fail)...")
try_withdraw()

# Wait 60 seconds
print("\n⏳ Waiting 60 seconds for unlock...")
for i in range(60, 0, -1):
    print(f"\rTime remaining: {i} seconds", end="")
    time.sleep(1)
print("\n")

# Try withdrawal again (should succeed)
print("🔓 Trying withdrawal again...")
try_withdraw()

# Check final state
check_vault_state()

print("\n" + "=" * 50)
print("✅ DEMO COMPLETE - VAULT WORKS!")
print("=" * 50)
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

# ===== YOUR NEW ALGO VAULT =====
APP_ID = 755414724
APP_ADDRESS = "7WD5INOSYBRKBBHJO7JL75XQ2M5WVELUQANCEO25LBG3525JJJ4Q5TRT5I"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def check_vault_state():
    """Check current vault state"""
    print("\n" + "=" * 50)
    print("📊 VAULT STATE")
    print("=" * 50)
    
    app_info = algod_client.application_info(APP_ID)
    global_state = app_info['params']['global-state']
    
    for item in global_state:
        key = base64.b64decode(item['key']).decode('utf-8')
        value = item['value']
        
        if value['type'] == 1:  # bytes
            if key == "beneficiary":
                addr_bytes = base64.b64decode(value['bytes'])
                addr = addr_bytes.decode('utf-8')
                print(f"  {key}: {addr}")
            elif key == "owner":
                print(f"  {key}: (set)")
            else:
                print(f"  {key}: {value['bytes']}")
        else:  # uint
            if key == "amount":
                print(f"  {key}: {value['uint'] / 1_000_000} ALGO")
            elif key == "unlock_time":
                unlock = value['uint']
                now = int(time.time())
                if now < unlock:
                    minutes = (unlock - now) // 60
                    print(f"  {key}: {unlock} (🔒 LOCKED - {minutes} minutes remaining)")
                else:
                    print(f"  {key}: {unlock} (🔓 UNLOCKED)")
            else:
                print(f"  {key}: {value['uint']}")

def deposit_to_vault(amount_algo):
    """Deposit ALGO to vault"""
    print("\n" + "=" * 50)
    print(f"💰 DEPOSITING {amount_algo} ALGO TO VAULT")
    print("=" * 50)
    
    amount_micro = int(amount_algo * 1_000_000)
    
    params = algod_client.suggested_params()
    
    # Transaction 1: App call
    app_call = ApplicationCallTxn(
        sender=student_address,
        sp=params,
        index=APP_ID,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=["deposit"]
    )
    
    # Transaction 2: ALGO payment
    payment = PaymentTxn(
        sender=student_address,
        sp=params,
        receiver=APP_ADDRESS,
        amt=amount_micro
    )
    
    # Group transactions
    gid = transaction.calculate_group_id([app_call, payment])
    app_call.group = gid
    payment.group = gid
    
    # Sign both
    signed_app_call = app_call.sign(PRIVATE_KEY)
    signed_payment = payment.sign(PRIVATE_KEY)
    
    # Send
    txid = algod_client.send_transactions([signed_app_call, signed_payment])
    wait_for_confirmation(algod_client, txid, 4)
    
    print(f"✅ Deposited {amount_algo} ALGO!")
    print(f"Transaction: https://testnet.algoexplorer.io/tx/{txid}")

def try_withdraw():
    """Try to withdraw from vault"""
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
        error_str = str(e)
        if "0 amount" in error_str:
            print("❌ No funds to withdraw")
        elif "timestamp" in error_str or "time" in error_str.lower():
            print("❌ REJECTED: Time lock not reached yet!")
        else:
            print(f"❌ Error: {error_str}")
        return False

# ===== DEMO =====
print("\n" + "🎓" * 25)
print("🎓 ALGO VAULT DEMO - TIME-LOCKED SAVINGS")
print("🎓" * 25)

# Check initial state
check_vault_state()

# Deposit 5 ALGO
deposit_to_vault(5)

# Check state after deposit
check_vault_state()

# Try immediate withdrawal (should fail)
print("\n⏰ Trying immediate withdrawal (should fail)...")
time.sleep(2)
try_withdraw()

# Check final state
check_vault_state()

print("\n" + "=" * 50)
print("✅ DEMO COMPLETE")
print("=" * 50)
print("\n📝 To withdraw after unlock time:")
print("   1. Wait 1 hour from deployment")
print("   2. Run: try_withdraw()")
print("\n🔗 View your vault:")
print(f"   https://testnet.algoexplorer.io/application/{APP_ID}")
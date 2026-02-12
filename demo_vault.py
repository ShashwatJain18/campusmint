def deposit_to_vault(amount_algo):
    """Deposit ALGO to vault"""
    print("\n" + "=" * 50)
    print(f"💰 DEPOSITING {amount_algo} ALGO TO VAULT")
    print("=" * 50)
    
    amount_micro = amount_algo * 1_000_000  # Convert ALGO to microALGO
    
    params = algod_client.suggested_params()
    
    # Transaction 1: App call
    app_call = ApplicationCallTxn(
        sender=student_address,
        sp=params,
        index=APP_ID,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=["deposit"]
    )
    
    # Transaction 2: ALGO transfer (not asset!)
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
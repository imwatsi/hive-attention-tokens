from hive_attention_tokens.chain.transactions.validators.definitions import AIRDROP, TRANSFER

TRANS_TYPES = {
    'air': AIRDROP,
    'trn': TRANSFER
}

def validate_transaction_permissions(acc, payload):
    trans_type = payload[0]
    if trans_type == 'air':
        if acc != "@@sys":
            raise Exception(f"'{acc}' not allowed to perform airdrop transaction")
    elif trans_type == 'trn':
        if acc != payload[1]: # from_account
            raise Exception("Cannot transfer tokens you don't own")

def validate_transaction_structure(payload):
    trans_type = payload[0]
    if trans_type not in TRANS_TYPES:
        raise Exception(f"Invalid transaction type ({trans_type})")
    definition = TRANS_TYPES[trans_type]
    total_pload_len = len(payload)
    expected_total_len = len(definition)
    if total_pload_len != expected_total_len:
        raise Exception (f"Transaction payload len ({total_pload_len}) invalid; expecting ({expected_total_len})")
    for i in range(len(definition)):
        expected_type = definition[i][0]
        actual_type = type(payload[i])
        #if not isinstance(payload[i], expected_type):
            #raise Exception (f"Payload ({i}); expected type {expected_type}, found {actual_type}")
        if expected_type is str:
            pload_len = len(payload[i])
            max_len = definition[i][1]
            if pload_len > max_len:
                raise Exception (f"Payload value ({i}); len ({pload_len}) exceeds max ({max_len})")
        elif expected_type is int:
            payload[i] = int(payload[i])
            def_max = definition[i][1]
            pload_value = payload[i]
            if pload_value > def_max:
                raise Exception (f"Payload value ({i}); ({payload[i]}) exceeds max ({def_max})")
        elif expected_type is float:
            payload[i] = float(payload[i])
            def_max = definition[i][1]
            def_max_dec = definition[i][2]
            pload_value = payload[i]
            if def_max:
                if pload_value > def_max:
                    raise Exception (f"Payload value ({i}); ({payload[i]}) exceeds max ({def_max})")
            if def_max_dec:
                dec_places = str(pload_value)[::-1].find('.')
                if int(dec_places) > def_max_dec:
                    raise Exception (f"Payload value ({i}); ({dec_places}) decimal places found, max is ({def_max_dec})")
    return payload
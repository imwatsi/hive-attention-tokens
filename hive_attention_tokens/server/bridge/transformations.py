from hive_attention_tokens.utils.tools import parse_transaction_payload

def transform_transaction(t_hash, raw_transaction):
    parsed = parse_transaction_payload(raw_transaction)
    if parsed[0] == 'air':
        return {
            'type': 'airdrop',
            'transaction_id': t_hash,
            'to_account': parsed[1],
            'token': parsed[2],
            'amount': parsed[3]
        }
    elif parsed[0] == 'trn':
        return {
            'type': 'transfer',
            'transaction_id': t_hash,
            'from_account': parsed[1],
            'to_account': parsed[2],
            'token': parsed[3],
            'amount': parsed[4]
        }
    return None
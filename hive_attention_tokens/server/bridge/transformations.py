def transform_transaction(raw_transaction):
    parsed = raw_transaction.split(',')
    if parsed[0] == 'air':
        return {
            'type': 'airdrop',
            'to_account': parsed[1],
            'token': parsed[2],
            'amount': parsed[3]
        }
    elif parsed[0] == 'trn':
        return {
            'type': 'transfer',
            'from_account': parsed[1],
            'to_account': parsed[2],
            'token': parsed[3],
            'amount': parsed[4]
        }
    return None
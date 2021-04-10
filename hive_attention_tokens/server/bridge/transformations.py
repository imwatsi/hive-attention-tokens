from hive_attention_tokens.utils.tools import parse_transaction_payload
from decimal import Decimal
import json
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID

def transform_transaction(t_hash, raw_transaction):
    parsed = parse_transaction_payload(raw_transaction)
    if parsed[0] == 'gen':
        return {
            'type': 'genesis',
            'transaction_id': t_hash,
            'token': parsed[1],
            'owner': parsed[2],
            'prop': json.loads(parsed[3])
        }
    elif parsed[0] == 'air':
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

def transform_balances(liquid, staked, savings):
    result = []
    combined = {}
    # TODO staked, savings
    for x in [liquid, staked, savings]:
        for t in x['token_map']:
            combined[t] = {
                'liquid': '0.000',
                'staked': '0.000',
                'savings': '0.000'
            }
        del x['token_map']


    for token in liquid:
        combined[token] = {'liquid': str(liquid[token])}

    for token in staked:
        combined[token]['staked'] = str(staked[token])

    for token in savings:
        combined[token]['savings'] = str(savings[token])
    
    for t in combined:
        liq = str(combined[t]['liquid'])
        stak = str(combined[t]['staked'])
        sav = str(combined[t]['savings'])
        result.append(
            {
                'token': t,
                'liquid': liq,
                'staked': stak,
                'savings': sav
            }
        )
    return result
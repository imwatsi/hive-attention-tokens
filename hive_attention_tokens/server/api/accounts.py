"""Account endpoints"""

from hive_attention_tokens.server.normalize import populate_by_schema, normalize_types
from hive_attention_tokens.server.bridge.transformations import transform_transaction

def verify_account_name(acc):
    assert isinstance(acc,str), "Hive account name must be a string"
    assert len(acc) <= 16, "invalid Hive account name provided"
    # TODO: invalid characters

async def get_account(context, account):
    verify_account_name(account)
    # TODO
    return {
        'account': account,
        'token_balances': [
            {
                'token': 'AA0000000000',
                'liquid': 100.000,
                'staked': 300.000,
                'savings': 100.000
            },
            {
                'token': 'ZZ9990000000',
                'liquid': 22.000,
                'staked': 455.000,
                'savings': 66.000
            },
            {
                'token': 'DD1234567812',
                'liquid': 1000.000,
                'staked': 30000.000,
                'savings': 10022.000
            }
        ],
        'properties': {
            'created': '2021-03-15T14:24:22',
            'authorities': {
                'owner': 'STM00000000000000000000000000000000000000000000000000',
                'active': 'STM00000000000000000000000000000000000000000000000000',
                'posting': 'STM00000000000000000000000000000000000000000000000000',
                'memo': 'STM00000000000000000000000000000000000000000000000000'
            }
        }
    }

async def get_account_history(context, account):
    verify_account_name(account)
    db = context['db']
    _trans = db.db.select(
        f"""SELECT b.timestamp, t.hash, t.data
                FROM transactions t
                LEFT JOIN blocks b ON t.block_num = b.index
                WHERE t.account = '{account}'
                ORDER BY b.index DESC
                LIMIT 50
            ;"""
    )
    if not _trans: return []
    
    transactions = []
    if _trans:
        for tr in _trans:
            full_tr = transform_transaction(tr[1], tr[2])
            full_tr['timestamp'] = tr[0]
            transactions.append(normalize_types(full_tr))

    result = {
        'account': account,
        'transactions': transactions
    }
    return result

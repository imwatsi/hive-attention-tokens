"""Account endpoints"""

from hive_attention_tokens.server.normalize import populate_by_schema, normalize_types
from hive_attention_tokens.server.bridge.transformations import transform_transaction

def verify_account_name(acc):
    assert len(acc) <= 16, "invalid Hive account name provided"
    # TODO: invalid characters

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
            transactions.append(full_tr)

    result = {
        'account': account,
        'transactions': normalize_types(
            transactions
        )
    }
    return result

"""Account endpoints"""

from hive_attention_tokens.chain.base.state import TokenBalances
from hive_attention_tokens.chain.base.auth import HiveAccounts
from hive_attention_tokens.server.normalize import populate_by_schema, normalize_types
from hive_attention_tokens.server.bridge.transformations import transform_transaction, transform_balances
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID
from decimal import Decimal

def verify_account_name(acc):
    assert isinstance(acc,str), "Hive account name must be a string"
    assert len(acc) <= 16, "invalid Hive account name provided"
    # TODO: invalid characters

async def get_account(context, account):
    verify_account_name(account)
    balances = TokenBalances.get_balances(account)
    token_bals = transform_balances(
        balances['liquid'],
        balances['staked'],
        balances['savings']
    )
    authorities = {}
    for kt in ['owner', 'active', 'posting', 'memo']:
        authorities[kt] = HiveAccounts.get_account_key(account, kt)

    return {
        'account': account,
        'token_balances': token_bals,
        'properties': {
            'created': '2021-03-15T14:24:22',
            'authorities': authorities
        }
    }

async def get_account_history(context, account):
    verify_account_name(account)
    db = context['db']
    _trans = db.db.select(
        f"""SELECT b.timestamp, t.hash, t.data
                FROM transactions t
                LEFT JOIN blocks b ON t.block_num = b.index
                WHERE t.account = '{account}' OR t.counter_account = '{account}'
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

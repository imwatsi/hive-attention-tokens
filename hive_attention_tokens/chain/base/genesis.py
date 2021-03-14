import json
import os

from hive_attention_tokens.ibc.hive.hive_api import HiveApi
from hive_attention_tokens.chain.database.access import DbAccess
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID

db = DbAccess.db

def get_genesis_accounts():
    # TODO: use on-chain method
    HOME_DIR = os.environ.get('HAT_HOME') or "/etc/hive-attention-tokens"
    return json.loads(open(f"{HOME_DIR}/genesis_accs.txt").read().strip())

def create_genesis_accounts(gen_accs):
    # TODO: retrieve pub keys and add to accounts table
    keys = HiveApi.get_accounts_keys(gen_accs)
    for new_acc in keys:
        owner_key = keys[new_acc]['owner']
        active_key = keys[new_acc]['active']
        posting_key = keys[new_acc]['posting']
        memo_key = keys[new_acc]['memo']
        db.new_hive_account(new_acc, owner=owner_key, active=active_key, posting=posting_key, memo=memo_key)

def get_genesis_airdrop_transactions(gen_accs):
    from hive_attention_tokens.chain.transactions.core import BaseTransaction
    trans = []
    tra_index = 0
    new_trans = BaseTransaction(
        '@@sys',
        None,
        None,
        f"air,@@sys,{NATIVE_TOKEN_ID},1000000.000",
        index=tra_index
    )
    trans.append(new_trans)
    if isinstance(gen_accs, list):
        if len(gen_accs) > 0:
            for acc in gen_accs:
                tra_index += 1
                new_trans = BaseTransaction(
                    '@@sys',
                    None,
                    None,
                    f"air,{acc},{NATIVE_TOKEN_ID},10.000",
                    index=tra_index
                )
                trans.append(new_trans)
            return trans
    raise Exception("No genesis accounts detected.")

def get_genesis_transactions():
    accs = get_genesis_accounts()
    result = []
    create_genesis_accounts(accs)
    airdrops = get_genesis_airdrop_transactions(accs)
    result.extend(airdrops)
    return result
"""Base chain endpoints"""

from hive_attention_tokens.chain.base.blockchain import BlockchainState
from hive_attention_tokens.chain.transactions.core import BaseTransaction
from hive_attention_tokens.chain.base.witness import TransactionMemPool
from hive_attention_tokens.server.normalize import populate_by_schema, normalize_types
from hive_attention_tokens.server.bridge.transformations import transform_transaction


async def get_info(context):
    return BlockchainState.get_chain_state()

async def submit_transaction(context, auth, account, transaction, signature, ref_block_id, ref_block_num):
    # TODO: validate at transaction object init level
    new_trans = BaseTransaction(account, signature, auth, transaction)
    # TODO: add transaction to mempool
    TransactionMemPool.add_transaction(new_trans)
    return "Transaction received and authenticated"

async def get_block(context, block_num):
    assert isinstance(block_num, int), "block_num must be an integer"
    db = context['db']
    _block = db.db.select(
        f"""SELECT hash, timestamp, previous_hash
            FROM blocks
            WHERE index = {block_num}
            ;"""
    )
    block =_block[0] if _block else None
    if not block: return {}
    _transactions = db.db.select(
        f"""SELECT hash, index, data, signature, account
            FROM transactions
            WHERE block_num = {block_num}
            ;"""
    ) or []
    transactions = []
    for i in range(len(_transactions)):
        transactions.append(
            transform_transaction(_transactions[i][0], _transactions[i][2])
        )
    
    _virtual_transactions = db.db.select(
        f"""SELECT index, data
            FROM virtual_transactions
            WHERE block_num = {block_num}
            ;"""
    ) or []
    virtual_transactions = []
    for i in range(len(_virtual_transactions)):
        virtual_transactions.append(
            transform_transaction(_virtual_transactions[i][0], _virtual_transactions[i][2])
        )

    result = {
        'block': normalize_types({
            'block_num': block_num,
            'block_hash': block[0],
            'timestamp': block[1],
            'previous_hash': block[2],
            'transactions_no': len(transactions),
            'virtual_transactions_no': len(virtual_transactions)
        }),
        'transactions': normalize_types(
            transactions
        ),
        'virtual_transactions': normalize_types(
            virtual_transactions
        )
    }
    return  result

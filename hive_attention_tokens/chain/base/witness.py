"""Triggers block production and processing and handles transaction signing and block verification."""

import time
from datetime import datetime, timedelta
from threading import Thread

from hive_attention_tokens.chain.base.blockchain import Block, Blockchain, BlockchainState
from hive_attention_tokens.config import Config
from hive_attention_tokens.utils.tools import UTC_TIMESTAMP_FORMAT

# TODO: start and maintain a schedule
# - verify transactions and compose a block
# - compute hash
# - sign it
# - add to blockchain
# - broadcast

config = Config.config

class BlockSchedule:

    last_timestamp = None
    running = False

    @classmethod
    def block_schedule(cls):
        if cls.running:
            print("Blocks schedule already running.")
            return
        BlockchainState.state_live_sync()
        while True:
            due = cls._check_block_time()
            if due:
                trans = []
                trans_index = 0
                while TransactionMemPool.transactions:
                    # TODO: process()
                    t = TransactionMemPool.transactions.pop()
                    t.index = trans_index
                    trans.append(t)
                    trans_index += 1
                    if trans_index == 50: break # temp block size cap
                _timestamp = cls.get_current_timestamp()
                new_block = Block(
                    BlockchainState.head_block_num + 1,
                    _timestamp,
                    Blockchain.last_block.compute_hash(),
                    trans,
                    config['witness_name']
                )
                del trans
                signature = new_block.sign_block(config['signing_key'], config['public_signing_key'])
                Blockchain.add_block_to_chain(new_block, config['witness_name'], signature)
                cls.last_timestamp = _timestamp
            time.sleep(0.1)

    @classmethod
    def _check_block_time(cls):
        if cls.last_timestamp is None: return True
        cur_time = datetime.utcnow()
        return True if cur_time >= datetime.strptime(cls.last_timestamp, UTC_TIMESTAMP_FORMAT) + timedelta(seconds=1) else False
    
    @classmethod
    def get_current_timestamp(cls):
        return datetime.utcnow().strftime(UTC_TIMESTAMP_FORMAT)

class BlockBroadcast:

    @classmethod
    def broadcast_block(cls, block):
        # TODO: get storable_block and broadcast
        pass

    @classmethod
    def receive_block(cls, block):
        # TODO: verify and process block
        pass

class TransactionMemPool:

    transactions = []

    @classmethod
    def add_transaction(cls, transaction):
        cls.transactions.append(transaction)
        
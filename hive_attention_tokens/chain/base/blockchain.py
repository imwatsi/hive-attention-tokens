import json
import ecdsa
import base64
from hashlib import sha256
from datetime import datetime
from binascii import hexlify, unhexlify
from hive_attention_tokens.chain.database.access import DbAccess
from hive_attention_tokens.chain.base.auth import WitnessSigning, WitnessVerification
from hive_attention_tokens.chain.base.genesis import get_genesis_transactions
from hive_attention_tokens.chain.transactions.core import BaseTransaction
from hive_attention_tokens.utils.base58 import Base58
from hive_attention_tokens.config import Config
from hive_attention_tokens.utils.tools import UTC_TIMESTAMP_FORMAT, BLANK_HASH, timestamp_to_string


BLOCK_KEYS_IGNORE = ["_transactions"]
chain_id = "0xhat0testnet" # TODO: import from utils
config = Config.load_config()
db = DbAccess.db

class Block:
    def __init__(self, index, timestamp, previous_hash,
                transactions, witness, signature=None):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.witness = witness
        self.signature = signature if signature else None
        self._transactions = transactions
        self.prep_transactions()
        self.transactions = self.get_storable_transactions()
        self.get_storable()
    
    def export_db(self):
        pass

    def export_broadcast(self):
        pass

    def prep_transactions(self):
        # add block index to transactions
        for t in self._transactions:
            t.block_num = self.index
    
    def get_storable(self):
        _keys = {}
        for k in self.__dict__:
            if k not in BLOCK_KEYS_IGNORE:
                _keys[k] = self.__dict__[k]
        self.storable = json.dumps(_keys, sort_keys=True)

    def get_storable_transactions(self):
        res = []
        for t in self._transactions:
            res.append(t.raw_transaction)
        return res

    def compute_hash(self):
        """
        A function that returns the hash of the block contents.
        """
        block_string = json.dumps(self.storable, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def sign_block(self, private_key, public_key):
        # TODO: move to witness.WitnessSigning
        privkey = unhexlify(repr(Base58(private_key)))
        sk = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
        block_string = self.storable
        #message = chain_id + block_string
        message = chain_id + block_string
        digest = sha256(message.encode('ascii')).digest()
        sig = sk.sign_digest_deterministic(digest, sigencode=ecdsa.util.sigencode_string)
        signature = base64.b64encode(sig).decode()

        pubkey = unhexlify(repr(Base58(public_key, prefix="STM")))
        pk = ecdsa.VerifyingKey.from_string(pubkey, curve=ecdsa.SECP256k1, hashfunc=sha256)
        valid = pk.verify_digest(sig,digest)
        assert valid, "invalid block signature" # TODO: temp, remove
        self.signature = signature
        return sig

    def verify_block(self, block, witness, signature):
        """Verifies blocks received from other nodes."""
        pass


class Blockchain: 
    """Stores top level state of blockchain and has methods to interact with block storage."""
    # TODO: implement chain_id; hash(chain_id+buffer) in transactions

    chain = [] # TEMP ??
    last_block = None
    current_transaction_index = {'block': 0, 'transaction': 0}

    @classmethod
    def add_block_to_chain(cls, block, witness, signature):
        # TODO: run through transaction objects and invoke process()
        # which effects the state
        # .get_storable (dict) and store
        # broadcast block
        block_hash = block.compute_hash()
        db._insert(
            'blocks',
            {
                'index': block.index,
                'hash': block_hash,
                'timestamp': block.timestamp,
                'previous_hash': block.previous_hash,
                'witness': block.witness,
                'signature': block.signature
            }
        )
        for tra in block._transactions:
            cls.current_transaction_index['block'] = block.index
            cls.current_transaction_index['transaction'] = tra.index
            #tra.save_transaction_to_db()
            tra.evoke_effectors()
        db._save() # TODO: temp, consider LIB as point of save
        # TODO: broadcast block
        BlockchainState.update_cur_block(block.index, block_hash, block.timestamp)
        cls.last_block = block
    
    @classmethod
    def process_existing_block(cls, block_num):
        # TODO: use WitnessVerification to verify block authenticity
        # TODO: process all transactions
        db_block = db.get_block(block_num)
        _trans = db.get_transactions_block(block_num)
        trans = []
        for t in _trans:
            trans.append(
                BaseTransaction(
                    t['account'],
                    t['signature'],
                    None,
                    t['data'],
                    t['index'],
                    t['block_num']
                )
            )
        ex_block = Block(
            db_block['index'],
            timestamp_to_string(db_block['timestamp']),
            db_block['previous_hash'],
            trans,
            db_block['witness'],
            db_block['signature']
        )
        WitnessVerification.verify_block(ex_block)
        # TODO: check if all transactions are processed (ref tables)
        cls.last_block = ex_block

    @classmethod
    def has_db_blocks(cls):
        head = db.get_db_head()
        return head if head else False
 
    @classmethod
    def create_genesis_state(cls):
        # TODO: create sys accounts (@null)
        db._insert(
            'hive_accounts',
            {
                'name': '@@sys',
                'owner': 'STM00000000000000000000000000000000000000000000000000',
                'active': 'STM00000000000000000000000000000000000000000000000000',
                'posting': 'STM00000000000000000000000000000000000000000000000000',
                'memo': 'STM00000000000000000000000000000000000000000000000000'
            }
        )
        # TODO: populate initial transactions
        init_transactions = get_genesis_transactions()
        genesis_block = Block(
            0,
            datetime.utcnow().strftime(UTC_TIMESTAMP_FORMAT),
            BLANK_HASH,
            init_transactions,
            config['witness_name']
        )
        block_hash = genesis_block.compute_hash()
        signature = genesis_block.sign_block(config['active_key'], config['public_active_key'])
        cls.add_block_to_chain(genesis_block, config['witness_name'], signature)

class BlockchainState:

    head_block_num = None
    head_block_id = None
    head_block_time = None
    state = None # replay / live sync

    @classmethod
    def update_cur_block(cls, num, _id, _time):
        cls.head_block_num = num
        cls.head_block_id = _id
        cls.head_block_time = _time
    
    @classmethod
    def get_chain_state(cls):
        info = {
            'head_block_num': BlockchainState.head_block_num,
            'head_block_id': BlockchainState.head_block_id,
            'head_block_time': BlockchainState.head_block_time
        }
        return info
    
    @classmethod
    def state_genesis(cls):
        cls.state = 'genesis'

    @classmethod
    def state_replaying(cls):
        cls.state = 'replay'
    
    @classmethod
    def state_live_sync(cls):
        cls.state = 'live sync'
    
    @classmethod
    def is_genesis(cls):
        return cls.state == 'genesis'
    @classmethod
    def is_replaying(cls):
        return cls.state == 'replay'
    
    @classmethod
    def is_live_syncing(cls):
        return cls.state == 'live sync'

class BlockchainData:

    @classmethod
    def get_block(cls, num):
        block_fields = ['index', 'hash', 'timestamp', 'previous_hash']
        res = db._select('blocks', columns=block_fields, col_filters={'index': num})
        if not res: return None
        block = db._populate_by_schema(res[0], block_fields)
        
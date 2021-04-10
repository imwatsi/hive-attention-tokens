"""Core transaction classes of the HAT chain"""
import json
from hashlib import sha256
from hive_attention_tokens.chain.base.auth import TransactionAuth, HiveAccounts
from hive_attention_tokens.chain.transactions.db_plug import DbTransactions
from hive_attention_tokens.chain.transactions.operations import OPERATION_DATA_RULES
from hive_attention_tokens.utils.tools import validate_data_rules, parse_transaction_payload
from hive_attention_tokens.chain.transactions.validators.validate import TRANS_TYPES, validate_transaction_structure, validate_transaction_permissions
from hive_attention_tokens.chain.transactions.validators.definitions import get_counter_account
from hive_attention_tokens.chain.transactions.effectors.evoke import EvokeTransaction

TRANSACTION_KEYS_IGNORE = []

class BaseTransaction:
    """The base transaction structure that all transactions start as."""
    def __init__(self, hive_acc, signature, authority, raw_trans, index=None, block_num=None):
        self.index = index
        self.block_num = block_num
        self.raw_transaction = raw_trans
        self.parsed_transaction = None
        self.packed_transaction = None
        self.transaction_type = None
        self.account = hive_acc
        self.signature = signature
        self.validate_transaction()
        self.get_auth_level()
        if authority:
            self.authority = authority
        else:
            auth = HiveAccounts.get_account_key(hive_acc,self.auth_level)
            if auth:
                self.authority = auth
            else:
                raise Exception("Unable to verify transaction authority.")
        self.validate_signature()
        
    
    def evoke_effectors(self):
        self.get_packed_transaction()
        self.get_hash()
        EvokeTransaction.evoke(self, self.account, self.block_num, self.hash, self.parsed_transaction)
    
    def get_packed_transaction(self):
        self.packed_transaction = {
            'block_num': self.block_num,
            'index': self.index,
            'data': self.raw_transaction,
            'signature': self.signature,
            'account': self.account
        }

    def save_transaction_to_db(self):
        DbTransactions.new_transaction({
            'hash': self.hash,
            'block_num': self.packed_transaction['block_num'],
            'index': self.packed_transaction['index'],
            'data': self.packed_transaction['data'],
            'signature': self.packed_transaction['signature'],
            'account': self.packed_transaction['account'],
            'counter_account': self.counter_account
        })

    def get_hash(self):
        data_string = json.dumps(self.packed_transaction, sort_keys=True)
        self.hash = sha256(data_string.encode()).hexdigest()
    
    def _parse_raw_transaction(self):
        # TODO optimize
        raw = self.raw_transaction
        parsed = parse_transaction_payload(raw)
        if len(parsed) < 1:
            raise Exception("Invalid transaction")
        return parsed
    
    def validate_transaction(self):
        trans = self._parse_raw_transaction()
        self.parsed_transaction = validate_transaction_structure(trans)
        validate_transaction_permissions(self.account, self.parsed_transaction)
        self.transaction_type = self.parsed_transaction[0]
        self.counter_account = get_counter_account(trans)

    def get_auth_level(self):
        if self.transaction_type == 'gen':
            self.auth_level = 'active'
        elif self.transaction_type == 'air':
            self.auth_level = 'active'
        elif self.transaction_type == 'trn':
            self.auth_level = 'active'
    
    def validate_signature(self):
        valid = TransactionAuth.verify_transaction(
            self.raw_transaction,
            self.account,
            self.signature,
            self.authority,
            self.auth_level
        )
        if valid is not True: raise Exception("Invalid transaction signature")

    def export_broadcast(self):
        pass


class AccountInit:

    def __init__(self, hive_account):
        pass

    def verify_authority(self):
        pass

class CreateToken:

    def __init__(self, hive_account):
        pass

    def verify_authority(self):
        pass
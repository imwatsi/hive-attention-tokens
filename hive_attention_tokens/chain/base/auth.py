import base64
import ecdsa
import json
from hashlib import sha256
from binascii import hexlify, unhexlify

from hive_attention_tokens.config import Config
from hive_attention_tokens.utils.base58 import Base58
from hive_attention_tokens.ibc.hive.hive_api import HiveApi
from hive_attention_tokens.chain.database.access import DbAccess


chain_id = "0xhat0testnet" # TODO: import from utils
db = DbAccess.db

class HiveAccounts:

    accounts = {}

    @classmethod
    def init(cls, state):
        cls.BlockchainState = state

    @classmethod
    def fetch_account(cls, acc_name):
        # check DB first
        db_acc = db.get_account(acc_name)
        if db_acc:
            cls.accounts[acc_name] = {
                'memo': db_acc['memo'],
                'posting': db_acc['posting'],
                'active': db_acc['active'],
                'owner': db_acc['owner']
            }
        else:
            keys = HiveApi.get_accounts_keys([acc_name])
            if keys:
                cls.accounts[acc_name] = keys[acc_name]
    
    @classmethod
    def get_account_key(cls, acc_name, key_type):
        if acc_name not in cls.accounts:
            if cls.BlockchainState.is_replaying() or cls.BlockchainState.is_genesis():
                cls.fetch_account(acc_name)
            else:
                return None
        if acc_name in cls.accounts:
            return cls.accounts[acc_name][key_type]

    @classmethod
    def update_keys(cls):
        pass

    @classmethod
    def verify_account_key(cls, acc_name, pub_key, auth):
        if acc_name not in cls.accounts:
            cls.fetch_account(acc_name)
        acc_keys = cls.accounts[acc_name]
        if pub_key == acc_keys[auth]:
            return True
        return False

class TransactionAuth:
    @classmethod
    def verify_transaction(cls, transaction, acc_name, signature, authority, auth_level):
        if acc_name == '@@sys':
            # TODO: crosscheck with individual token issuer data
            return True
        authenticated = HiveAccounts.verify_account_key(acc_name, authority, auth_level)
        if not authenticated: return False
        sig = base64.b64decode(signature)
        pubkey = unhexlify(repr(Base58(authority, prefix="STM")))
        pk = ecdsa.VerifyingKey.from_string(pubkey, curve=ecdsa.SECP256k1, hashfunc=sha256)
        message = chain_id + transaction
        digest = sha256(message.encode('ascii')).digest()
        try:
            valid = pk.verify_digest(sig,digest)
            return valid
        except:
            return False

class WitnessSigning:

    @classmethod
    def sign_block(cls, block):
        pass

class WitnessVerification:

    @classmethod
    def verify_block(cls, block):
        pass
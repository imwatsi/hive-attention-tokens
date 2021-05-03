import json
from hive_attention_tokens.chain.base.state import StateMachine
from hive_attention_tokens.utils.tools import get_hash_sha256
from hive_attention_tokens.chain.transactions.db_plug import DbTransactions
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID, SYSTEM_ACCOUNT
from hive_attention_tokens.utils.tools import normalize_json


class NativeTokenV1:
    def __init__(self, parent, orig_acc, block_num, transaction_id, trans):
        """ trans_type, to_account, token, amount """
        trn_name = trans[0]
        if trn_name == 'gen':
            self.op = self.Genesis(parent, orig_acc, transaction_id, trans[2], trans[3])
        elif trn_name == 'air':
            self.op = self.Airdrop(parent, orig_acc, transaction_id, trans[1], trans[3])
        elif trn_name == 'trn':
            self.op = self.Transfer(parent, orig_acc, transaction_id, trans[1], trans[2], trans[4])
        else:
            raise Exception (f"Invalid transaction type passed to Native Token effector: {trn_name}")

    class Genesis:
        def __init__(self, parent, orig_acc, transaction_id, owner, props):
            self.parent = parent
            self.orig_acc = orig_acc
            self.transaction_id = transaction_id
            self.owner = owner
            self.props = props
            self.action = None
            self.validate()
        
        def validate(self):
            if self.orig_acc != SYSTEM_ACCOUNT: raise Exception ("Token generation account and owner must the same.")
            self.action = StateMachine.token_genesis_action(NATIVE_TOKEN_ID, self.props)

        def process(self):
            self.action.process()
            # all checks passed, save to DB
            self.parent.save_transaction_to_db()
            DbTransactions.new_token_transfer({
                'token_id': NATIVE_TOKEN_ID,
                'transaction_id': self.transaction_id,
                'from_acc': SYSTEM_ACCOUNT,
                'to_acc': SYSTEM_ACCOUNT,
                'amount': self.props['initial_supply']
            })
            data = {
                'id': NATIVE_TOKEN_ID,
                'owner': self.owner,
                'init_transaction_id': self.transaction_id,
                'props': normalize_json(self.props)
            }
            DbTransactions.new_token_genesis(data)


    class Airdrop:
        def __init__(self, parent, orig_acc, transaction_id, account, amount):
            self.parent = parent
            self.orig_acc = orig_acc
            self.transaction_id = transaction_id
            self.account = account
            self.amount = amount
            self.action = None
            self.validate()
        
        def validate(self):
            if self.orig_acc != SYSTEM_ACCOUNT:  raise Exception("Only the system account can airdrop native tokens.")
            self.action = StateMachine.airdrop_action(NATIVE_TOKEN_ID, self.account, self.amount)
        
        def process(self):
            # run past state machine / validate
            self.action.process()
            # all checks passed, save to DB
            self.parent.save_transaction_to_db()
            data = {
                'token_id': NATIVE_TOKEN_ID,
                'transaction_id': self.transaction_id,
                'from_acc': SYSTEM_ACCOUNT,
                'to_acc': self.account,
                'amount': self.amount
            }
            DbTransactions.new_token_transfer(data)

    class Transfer:
        def __init__(self, parent, orig_acc, transaction_id, from_acc, to_acc, amount):
            self.parent = parent
            self.orig_acc = orig_acc
            self.transaction_id = transaction_id
            self.from_acc = from_acc
            self.to_acc = to_acc
            self.amount = amount
            self.action = None
            self.validate()
        
        def validate(self):
            if self.orig_acc != self.from_acc:
                # TODO: check multisig, else exception
                raise Exception(f"'{self.orig_acc}' is not allowed to transfer tokens from '{self.from_acc}'")
            self.action = StateMachine.transfer_action(NATIVE_TOKEN_ID, self.from_acc, self.to_acc, self.amount)

        def process(self):
            self.action.process()
            # all checks passed, save to DB
            self.parent.save_transaction_to_db()
            data = {
                'token_id': NATIVE_TOKEN_ID,
                'transaction_id': self.transaction_id,
                'from_acc': SYSTEM_ACCOUNT,
                'to_acc': self.to_acc,
                'amount': self.amount
            }
            DbTransactions.new_token_transfer(data)

    class Stake:
        pass

    class WitnessReward:
        pass

    class VoteWitness:
        pass

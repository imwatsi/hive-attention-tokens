import json
from hive_attention_tokens.utils.tools import get_hash_sha256
from hive_attention_tokens.chain.transactions.db_plug import DbTransactions
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID


class NativeTokenV1:
    def __init__(self, block_num, transaction_id, trans):
        """ trans_type, to_account, token, amount """
        trn_name = trans[0]
        if trn_name == 'air':
            self.op = self.Airdrop(block_num, transaction_id, trans[1], trans[3])
        elif trn_name == 'trn':
            self.op = self.Transfer(trans)
        else:
            raise Exception (f"Invalid transaction type passed to Native Token effector: {trn_name}")

    class Airdrop:
        def __init__(self, block_num, transaction_id, account, amount):
            self.transaction_id = transaction_id
            self.account = account
            self.amount = amount
        
        def process(self):
            data = {
                'token_id': NATIVE_TOKEN_ID,
                'transaction_id': self.transaction_id,
                'from_acc': '@@sys',
                'to_acc': self.account,
                'amount': self.amount
            }
            DbTransactions.new_token_transfer(data)


    class Transfer:
        def __init__(self, trans):
            # TODO: load up variables
            self.raw_transaction = trans
            self.validate()

        def validate(self):
            pass

        def process(self):
            pass

    class Stake:
        pass

    class WitnessReward:
        pass

    class VoteWitness:
        pass

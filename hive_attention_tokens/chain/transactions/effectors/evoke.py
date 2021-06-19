from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID
from hive_attention_tokens.chain.transactions.effectors.native_token import NativeTokenV1

class EvokeTransaction:

    @classmethod
    def evoke(cls, parent, orig_acc, block_num, trans_id, transaction):
        # token operations (airdrop, transfer, stake, mint)
        if transaction[0] == 'gen':
            if transaction[1] == NATIVE_TOKEN_ID:
                NativeTokenV1(parent, orig_acc, block_num, trans_id, transaction).op.process()
        if transaction[0] == 'air':
            if transaction[2] == NATIVE_TOKEN_ID:
                NativeTokenV1(parent, orig_acc, block_num, trans_id, transaction).op.process()
        elif transaction[0] == 'trn':
            if transaction[3] == NATIVE_TOKEN_ID:
                NativeTokenV1(parent, orig_acc, block_num, trans_id, transaction).op.process()
        elif transaction[0] == 'vot':
            if transaction[3] == NATIVE_TOKEN_ID:
                NativeTokenV1(parent, orig_acc, block_num, trans_id, transaction).op.process()
                
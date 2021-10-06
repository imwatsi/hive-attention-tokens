from hive_attention_tokens.engine.witness_voting import WitnessVoteEffect
from hive_attention_tokens.engine.tokens import ClaimdropEffect

class TransactionsProcessor:

    @classmethod
    def process_transaction(cls, trans_id, block, timestamp, req_auths, req_posting_auths, trans_type, payload):
        if trans_type == 'claimdrop':
            acc = req_posting_auths[0]
            token_id = payload['token']
            ClaimdropEffect.do(trans_id, timestamp, acc, token_id)
        elif trans_type == 'wit_vote':
            witness = payload[0]
            vote = bool(payload[1])
            acc = req_auths[0]
            WitnessVoteEffect.do(timestamp, acc, witness, vote)
        elif trans_type == 'vote':
            _id = payload['id']
            permlink = payload['permlink']
            
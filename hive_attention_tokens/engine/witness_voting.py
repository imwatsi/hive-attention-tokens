
from hive_attention_tokens.database.handlers import AttentionTokensDb


class WitnessVoteEffect:

    @classmethod
    def init(cls, db: AttentionTokensDb):
        cls.db = db

    @classmethod
    def do(cls, timestamp, voter, witness, vote) -> None:
        has_entry = cls.db.get_acc_witness_vote(voter, witness)
        if has_entry:
            cls.db.update_witness_vote(voter, witness, vote)
        else:
            cls.db.add_new_witness_vote(voter, witness, vote)
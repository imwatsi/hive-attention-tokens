from hive_attention_tokens.database.handlers import AttentionTokensDb


class ClaimdropEffect:

    @classmethod
    def init(cls, db: AttentionTokensDb):
        cls.db = db

    @classmethod
    def do(cls, trans_id, acc, token) -> None:
        has_claimed = cls.db.get_acc_token_claimdrop(acc, token)
        if not has_claimed:
            cls.db.add_new_claimdrop(trans_id, acc, token)

class VoteEffect:

    @classmethod
    def init(cls, db: AttentionTokensDb):
        cls.db = db
    
    @classmethod
    def do(cls, trans_id, acc, token) -> None:
        valid_token = cls.db.is_valid_token(token)
        assert valid_token, f"invalid token {token}"
        
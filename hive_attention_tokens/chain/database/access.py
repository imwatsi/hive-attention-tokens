from hive_attention_tokens.chain.database.setup import DbSetup
from hive_attention_tokens.chain.database.handlers import AttentionTokensDb
from hive_attention_tokens.config import Config

config = Config.load_config()
DbSetup.check_db(config)

class DbAccess:

    db = AttentionTokensDb(config)

    @classmethod
    def init(cls, db):
        cls.db = db
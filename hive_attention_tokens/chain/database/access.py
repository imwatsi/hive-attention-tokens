from hive_attention_tokens.config import Config
from hive_attention_tokens.chain.database.setup import DbSetup
from hive_attention_tokens.chain.database.handlers import AttentionTokensDb

config = Config.config

class DbAccess:

    db = AttentionTokensDb(config)
    DbSetup.check_db(config)
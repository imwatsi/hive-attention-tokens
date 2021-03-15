from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from hive_attention_tokens.config import Config
from hive_attention_tokens.chain.database.setup import DbSetup
from hive_attention_tokens.chain.database.handlers import AttentionTokensDb

config = Config.config

class DbAccess:

    # temporarily drop db while in dev, pending replay optimization
    print("Dropping old DB")
    conn = connect(f"dbname=postgres user={config['db_username']} password={config['db_password']}")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE hive_attention_tokens;")
    cur.execute("CREATE DATABASE hive_attention_tokens;")
    print("New DB created")

    db = AttentionTokensDb(config)
    DbSetup.check_db(config)
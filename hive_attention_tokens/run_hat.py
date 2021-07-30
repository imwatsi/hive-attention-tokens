from hive_attention_tokens.network.serve import run_server
from hive_attention_tokens.network.peers import Peers
from hive_attention_tokens.config import Config

config = Config.config

def inits():
    Peers.load_own_info()
    Peers.load_seed_peers()

def run():
    inits()
    run_server(config)


if __name__ == "__main__":
    run()

from datetime import datetime
from os import truncate
import requests
import json

from hive_attention_tokens.config import Config
from hive_attention_tokens.utils.tools import UTC_TIMESTAMP_FORMAT

config = Config.config

class Peers:

    peers = []   #  {"host","last_ping","last_block"}
    me = {}
    boot_time = datetime.utcnow()

    @classmethod
    def load_own_info(cls):
        """Loads the witness node's own info from the config file and memory."""
        cls.me = {
            "witness_name": config['witness_name'],
            "up_since": datetime.strftime(cls.boot_time, UTC_TIMESTAMP_FORMAT)
        }

    @classmethod
    def load_seed_peers(cls):
        """Reads seed nodes from the config file and loads them in memory."""
        seeds = config['seed_nodes']
        for s in seeds:
            good_node = PeerTalk.ping_node(s)
            if good_node:
                cls.save_new_peer(good_node)

    @classmethod
    def get_current_peers(cls):
        """Returns a list of the current peers the node has in its memory."""
        return cls.peers

    @classmethod
    def get_own_info(cls):
        """Returns information about the current node."""
        return cls.me

    @classmethod
    def save_new_peer(cls, details):
        """Adds a new peer to memory."""
        cls.peers.append(details)

class PeerTalk:

    @classmethod
    def _make_request(cls, url, method, params={}):
        """Base method to make a request on the peer network."""
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        try:
            req = requests.post(url, json=data)
            if req.status_code == 200:
                resp = json.loads(req.content)
                return resp['result']
            print(req.content)
            print(req.status_code)
        except Exception as e:
            print(e)

    @classmethod
    def ping_node(cls, node):
        """Check if a node is online."""
        x = cls._make_request(node, "net_api.get_current_peers")
        print(x)
        return x
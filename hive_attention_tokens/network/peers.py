from datetime import datetime
from os import truncate
import json
import requests
import time

from hive_attention_tokens.config import Config
from hive_attention_tokens.utils.tools import UTC_TIMESTAMP_FORMAT

config = Config.config

class Peers:

    peers = {}   #  {"host","last_ping","last_block"}
    potential_peers = []
    me = {}
    boot_time = datetime.utcnow()

    @classmethod
    def load_own_info(cls):
        """Loads the witness node's own info from the config file and memory."""
        cls.me = {
            "witness_name": config['witness_name'],
            "up_since": datetime.strftime(cls.boot_time, UTC_TIMESTAMP_FORMAT),
            "last_block": None # TODO
        }

    @classmethod
    def load_seed_peers(cls):
        """Reads seed nodes from the config file and loads them in memory."""
        seeds = config['seed_nodes']
        for s in seeds:
            good_node = PeerTalk.ping_node(s)
            if good_node:
                cls.save_new_peer(s, good_node)
                cls.compare_peer_lists(good_node['peers'])

    @classmethod
    def get_current_peers(cls):
        """Returns a list of the current peers the node has in its memory."""
        return cls.peers

    @classmethod
    def get_own_info(cls):
        """Returns information about the current node."""
        return cls.me

    @classmethod
    def save_new_peer(cls, host, details):
        """Adds a new peer to memory."""
        cls.peers[host] = {
            'host' : host,
            'last_ping': details['last_ping'],
            'last_block': details['last_block']
        }
    
    @classmethod
    def compare_peer_lists(cls, new):
        for p in new:
            if p not in cls.potential_peers: cls.potential_peers.append(p)
    
    @classmethod
    def peer_list_refresher(cls):
        while True:
            for p in cls.peers:
                good = PeerTalk.ping_node(p)
                if not good:
                    cls.peers.remove(p)
                time.sleep(2)
            time.sleep(60)
    
    @classmethod
    def is_registered_node(cls, node):
        # TODO: check for on-chain broadcast
        return True


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
        reply = cls._make_request(node, "net_api.get_node_info")
        if reply:
            reply['last_ping'] = datetime.utcnow()
            if not Peers.is_registered_node(node): return None
        print(reply)
        return reply
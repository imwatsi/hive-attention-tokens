import json
import os
import requests
import time
from datetime import datetime, timedelta

HIVE_NODES = [
    "https://api.hive.blog", "https://anyx.io", "https://api.openhive.network",
    "https://hive.roelandp.nl", "https://rpc.ausbit.dev", "https://api.pharesim.me",
    "https://api.deathwing.me"
]

# TODO: multi node data verification

class NodeLoads:

    def __init__(self):
        self.counts = {}
        self.reset_counts()
        self.minute = datetime.utcnow().minute
    
    def reset_counts(self):
        self.counts.clear()
        for node in HIVE_NODES:
            self.counts[node] = 0

    def record_req(self, node):
        cur_minute = datetime.utcnow().minute
        if self.minute != cur_minute:
            self.reset_counts()
            self.minute = cur_minute
        self.counts[node] += 1
    
    def get_node_to_use(self):
        lowest = None
        for node in self.counts:
            cur_count = self.counts[node]
            if not lowest: lowest = [node, cur_count]
            if lowest[1] > cur_count: lowest = [node, cur_count]
        return lowest[0]
        
hive_nodes = NodeLoads()

def make_request(method, params=[]):
    count = 0
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": int(time.time())
    }
    while True:
        try:
            node = hive_nodes.get_node_to_use()
            hive_nodes.record_req(node)
            req = requests.post(node, data=json.dumps(payload), timeout=3)
            result = json.loads(req.content)['result']
            return result
        except Exception as e:
            # TODO: log error
            if count == 20:
                # TODO: error, safe shutdown, log
                print(e)
                os._exit(1)
            time.sleep(0.1)
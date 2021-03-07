from hive_attention_tokens.ibc.hive.hive_requests import make_request

class HiveApi:
    @classmethod
    def get_accounts_keys(cls, accounts):
        res = {}
        accs = make_request("condenser_api.get_accounts", [accounts])
        for acc in accs:
            res[acc['name']] = {
                'owner': acc['owner']['key_auths'][0][0],
                'active':acc['active']['key_auths'][0][0],
                'posting': acc['posting']['key_auths'][0][0],
                'memo': acc['memo_key']
            }
        return res

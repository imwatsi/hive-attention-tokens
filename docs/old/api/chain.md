# Chain API

## chain.get_info

Returns top level info about the blockchain

**Sample request:**

```
{
    "jsonrpc": "2.0",
    "method": "chain_api.get_info",
    "params": {},
    "id": 1
}
```

**Expected response:**

```
{
    "jsonrpc": "2.0",
    "result": {
        "head_block_num": 17091,
        "head_block_id": "e86c5fed1c6128fbc4371221d515b4ee02122292979b2573de0dbe32d94ffafc",
        "head_block_time": "2021-03-07T14:37:59"
    },
    "id": 1
}
```

## chain.get_block

Returns contents of a specified block

**Sample request:**

```
{
    "jsonrpc": "2.0",
    "method": "chain_api.get_block",
    "params": {"block_num": 100},
    "id": 1
}
```

**Expected response:**

```
{
    "jsonrpc": "2.0",
    "result": {
        "block": {
            "block_num": 100,
            "block_hash": "8ba560f08ba565062b004da23470c054349506ec4cf5fe8274bff7dba52ca184",
            "timestamp": "2021-03-07T09:52:30",
            "previous_hash": "76d721b168fbf8c550155038d2c44e5f7b78f43db8fdc7e4e2e4901cf1086ab5"
        },
        "transactions": [
            {
                "type": "transfer",
                "from_account": "imwatsi.test",
                "to_account": "null",
                "token": "AA0000000000",
                "amount": "2"
            }
        ],
        "virtual_transactions": []
    },
    "id": 1
}
```

---

## chain.get_transaction

Returns details about a specified transaction

**Sample request:**

```
{
    "jsonrpc": "2.0",
    "method": "chain_api.get_transaction",
    "params": {"transaction_id": "28c2df7413b4aee3325629e639ad298c1213c3c713c638955fd112d3aae08497"},
    "id": 1
}
```

**Expected response:**

```
{
    "jsonrpc": "2.0",
    "result": {
        "type": "transfer",
        "transaction_id": "28c2df7413b4aee3325629e639ad298c1213c3c713c638955fd112d3aae08497",
        "from_account": "imwatsi.test",
        "to_account": "hive-133333",
        "token": "AA0000000000",
        "amount": "0.006",
        "index": 0,
        "block_num": 177,
        "signature": "AT5pDOUDPcdebmWfyUBRM7QcU4Xq+0KPEn5k/7x6NnWRC38qzGugd1E+yHzCTqGfTPX27Dw4PVr7evFf6lboYA==",
        "account": "imwatsi.test",
        "raw_transaction": ""
    },
    "id": 1
}
```
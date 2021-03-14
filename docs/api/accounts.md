# Accounts API

## accounts.get_account_history

Returns a specified account's transaction history

**Sample request:**

```
{
    "jsonrpc": "2.0",
    "method": "accounts_api.get_account_history",
    "params": {"account": "imwatsi.test"},
    "id": 1
}
```

**Expected response:**

```
{
    "jsonrpc": "2.0",
    "result": {
        "account": "imwatsi.test",
        "transactions": [
            {
                "type": "transfer",
                "transaction_id": "d85a0708310913d3f65d3c85f5b59e4c19a5d804fb8b03141374b78fb432763a",
                "from_account": "imwatsi.test",
                "to_account": "imwatsi",
                "token": "AA0000000000",
                "amount": "0.01",
                "timestamp": "2021-03-14T15:22:32"
            },
            {
                "type": "transfer",
                "transaction_id": "20f68077cbfdbc613bb67eaad2f6780a7d74446cc5e46011ceb687d1a948d711",
                "from_account": "imwatsi.test",
                "to_account": "imwatsi",
                "token": "AA0000000000",
                "amount": "0.002",
                "timestamp": "2021-03-14T15:22:32"
            },
            {
                "type": "transfer",
                "transaction_id": "592edf3225c709295fa2577b67acf397881329db0b4d3ec87568abe87698a7f4",
                "from_account": "imwatsi.test",
                "to_account": "imwatsi",
                "token": "AA0000000000",
                "amount": "0.003",
                "timestamp": "2021-03-14T15:22:31"
            },
            {
                "type": "transfer",
                "transaction_id": "713daaa36beaf473371cb4dc1fc2cf5e6afeb88ece4df0e39dfcbcb8085ced38",
                "from_account": "imwatsi.test",
                "to_account": "imwatsi",
                "token": "AA0000000000",
                "amount": "0.012",
                "timestamp": "2021-03-14T15:22:31"
            }
        ]
    },
    "id": 1
}
```
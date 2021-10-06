# Custom JSON Ops

[
    [1, "hat/0.0.1"],
    "{op_name}",
    {{payload}}
]

## Chain Ops

### genesis

[WIP]

This is a once-off 

op_name: genesis
op_payload: {
    "chain_id": "",
    "init_witnesses": []
}

### witness_vote

Broadcasts a Hive account's vote for a witness.

op_name: wit_vote
op_payload: {
    "witness": "imwatsi",
    "value": 1|0
}


---

## Token Ops

### claimdrop

Claims tokens put up for distribution.

op_name: claimdrop
op_payload: {
    "token": "AA0000000000"
}

### create

op_name: token_create
op_payload:

```
{
    "id": "AA0000000000",
    "type": "pob",
    "props": {
        "supply": {
            "init_amount": "10000000.000",
            "emission": ["tail_constant", "0.01"],
            "emission_target_accs": [["@@rewards", "0.009"], ["@imwatsi.test", "0.001"]],
            "init_reward_pool": "10000.000"
        },
        "voting": "stake_weighted",
        "airdrop_accounts": [["imwatsi.test","1000.000"], ["imwatsi","1000.000"]]
    }
}
```

**emissions settings:**

`tail_constant`: `null` | `["tail_constant", token_amount]`
`emission_target_accs`: `[[acc, amount], [amount, acc]]` # must equal emission total above

**airdrops**

`airdrop_accounts`: `[[acc, amount], [amount, acc]]` # must be less than the supply's init_amount

---

### transfer

Transfers the HAT-based token to another Hive account.

op_name: transfer
op_payload: {
    "id": "AA0000000000",
    "from": "imwatsi",
    "to": "imwatsi",
    "amount": "100.000",
    "memo": "Test transfer"
}

### stake

op_name: stake
op_payload: {
    "id": "AA0000000000",
    "period": 100 [optional]
}

### vote

op_name: vote
op_payload: {
    "id": "AA0000000000",
    "permlink": "@imwatsi/cool-post"
}

---

## Witness Ops

### join

Used by a witness node to broadcast intent to join/rejoin the network.

op_name: wit_join
op_payload: {
    "public_key": "",
    "node": IP address or URL
}

### validate

Used by a witness node to validate a block of transactions.

op_name: wit_validate
op_payload: {
    "hive_block": 123123,
    "tot_trans": 100,
    "block_hash": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "signature": "zxczxczxczxczxczxczxczxczxczxczcxz"
}

### testify

Used by a witness to express the state of the HAT blockchain as they see it, as per Hive block height.

op_name: wit_testify
op_payload: {
    "hive_block": 1234123,
    "running_hash": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxX",
    "hat_height": 44444,
    "
}
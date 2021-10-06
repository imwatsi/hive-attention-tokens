# Broadcasting transactions to the HAT sidechain

## Token genesis

Creates a token on the HAT chain, with the defined properties. Properties are passed as a JSON object as the last element in the CSV payload.

`gen,{token_id},{owner_account},{"initial_supply": "n.nnn"}`

For example;

`gen,AA0000000000,sys,{"initial_supply": "1000000.000"}`

#### Token properties

`initial_supply`
*number of tokens to generate initially*

- `airdrop_accounts`: a few Hive account names to airdrop tokens to, and the amounts
    `[[account,"1000.000"]]`
- `distribution`: props that determine distribution of tokens
    - `emission`: [type, values...]
        - ["tail_constant", "0.001"]
        - ["", ""]
    - `rewards`: [type, values...]
        - [""]

---

## Token transfer

Moves tokens from one HAT account to another.

`trn,{from_account},{acc_to},{token_id},{amount}`

For example:

`trn,imwatsi.test,imwatsi,AA0000000000,100.000`

---

## Airdrop

---

## Vote (token)

Makes a vote for a specified Hive post, in a specified token's economy.

`vot,{origin_acc},{receiving_acc},{token_id},{permlink}`

For example:

`vot,imwatsi.test,hichem.test,ZZ9990000000,cool-post`
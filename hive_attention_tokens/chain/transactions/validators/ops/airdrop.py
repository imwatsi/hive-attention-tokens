""" trans_type, to_account, token, amount """
from decimal import Decimal
from hive_attention_tokens.utils.tools import Json, MAX_ACC_NAME, MAX_TOKEN_LEN, TOKEN_DECIMAL_PLACES, MAX_TOKEN_AMOUNT


class TokenAirdropOp:
    def __init__(self, op_payload):
        self.op = op_payload
        self.load_elements()
        self._validate_op_name()
        self._validate_to_acc()
        self._validate_token_id()
        self._validate_amount()
    
    def get_parsed_transaction(self):
        return [
            self.op_name,
            self.to_account,
            self.token_id,
            self.amount
        ]
    
    def load_elements(self):
        self.op_name = self.op[0]
        self.to_account = self.op[1]
        self.token_id = self.op[2]
        self.amount = self.op[3]
    
    def _validate_op_name(self):
        # check op_name
        if self.op_name != 'air':
            raise Exception (
                f"Expecting 'air' op type, found '{self.op_name}'"
            )

    def _validate_token_id(self):
        # check token_id
        if not isinstance(self.token_id, str):
            raise Exception(
                f"The transaction's 'token_id' is supposed to be a string, "
                f"found {type(self.token_id)}"
            )
        if len(self.token_id) > MAX_TOKEN_LEN:
            raise Exception(
                f"The transaction's 'token_id' len ({self.token_id}) is longer "
                f"than the max allowed ({self.token_id})"
            )
    
    def _validate_to_acc(self):
        # check to_account account
        if not isinstance(self.to_account, str):
            raise Exception(
                f"The transaction's 'to_account' is supposed to be a string, "
                f"found {type(self.to_account)}"
            )
        if len(self.to_account) > MAX_ACC_NAME:
            raise Exception(
                f"The transaction's 'to_account' len ({self.to_account}) is longer "
                f"than the max allowed ({MAX_ACC_NAME})"
            )

    def _validate_amount(self):
        # check amount (Decimal(3))
        self.amount = Decimal(self.amount)
        if MAX_TOKEN_AMOUNT and self.amount > MAX_TOKEN_AMOUNT:
            raise Exception (f"Payload value ({i}); ({payload[i]}) exceeds max ({MAX_TOKEN_AMOUNT})")
        dec_places = str(self.amount)[::-1].find('.')
        if int(dec_places) != TOKEN_DECIMAL_PLACES:
            raise Exception (f"Payload value ({i}); ({dec_places}) decimal places found, required is ({TOKEN_DECIMAL_PLACES})")
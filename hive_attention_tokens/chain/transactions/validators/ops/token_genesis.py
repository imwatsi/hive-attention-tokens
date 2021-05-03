""" trans_type, token_id, owner, props(json) """
from decimal import Decimal
from hive_attention_tokens.utils.tools import Json, MAX_TOKEN_LEN


class TokenGenesisOp:
    def __init__(self, op_payload):
        self.op = op_payload
        self.load_elements()
        self._validate_op_name()
        self._validate_token_id()
        self._validate_owner()
        self._validate_props()
    
    def get_parsed_transaction(self):
        return [
            self.op_name,
            self.token_id,
            self.owner,
            self.props
        ]
    
    def load_elements(self):
        self.op_name = self.op[0]
        self.token_id = self.op[1]
        self.owner = self.op[2]
        self.props = self.op[3]
    
    def _validate_op_name(self):
        # check op_name
        if self.op_name != 'gen':
            raise Exception (
                f"Expecting 'gen' op type, found '{self.op_name}'"
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
                f"than the max allowed ({MAX_TOKEN_LEN})"
            )
    
    def _validate_owner(self):
        # check owner account
        if not isinstance(self.owner, str):
            raise Exception(
                f"The transaction's 'owner' is supposed to be a string, "
                f"found {type(self.owner)}"
            )
        if len(self.owner) > MAX_TOKEN_LEN:
            raise Exception(
                f"The transaction's 'owner' len ({self.owner}) is longer "
                f"than the max allowed ({self.owner})"
            )

    def _validate_props(self):
        # check props (JSON)
        if len(self.props) > 2048:
            raise Exception(
                f"The transaction's 'props' len ({self.props}) is longer"
                f"than the max allowed ({self.props})"
            )
        self.props = Json(self.props).json_object
        # mandatory fields
        for f in ['initial_supply']:
            if f not in self.props:
                raise Exception(f"Transaction is missing the '{f}' prop")
        
        def initial_supply(value):
            dec = str(value)[::-1].find('.')
            if int(dec) != 3:
                raise Exception(
                    f"Transaction's initial_supply must have (3) decimal places, "
                    f"({dec}) were found"
                )
            try:
                self.props['initial_supply'] = Decimal(value)
            except:
                raise Exception("Transaction's 'initial_supply' prop not a valid token amount")

        # validate mandatory fields
        initial_supply(self.props['initial_supply'])
        # validate optional fields
        if '' in self.props:
            pass
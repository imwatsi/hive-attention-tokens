import re

from hive_attention_tokens.utils.tools import START_BLOCK


OP_START_BLOCKS = {
    'wit_vote': START_BLOCK,
    'genesis': ''
}

class Validation:

    class WitnessVoteValidation:

        def __init__(self, req_auths, payload) -> None:
            self.req_auths = req_auths
            self.payload = payload
        
        def validate(self):
            assert len(self.req_auths) == 1, 'one required_auths is needed for wit_vote op'

    @classmethod
    def _validate_app_version(cls, value):
        valid = re.match(r'hat/[0-9]{1,1}.[0-9]{1,1}.[0-9]{1,1}', value)
        assert valid, 'invalid app version in op header'

    @classmethod
    def _validate_header(cls, block, header):
        assert isinstance(header, list), 'invalid header, must be a list'
        op_version = header[0]
        app_version = header[1]
        assert isinstance(op_version, int), 'op version in header must be an integer'
        assert isinstance(app_version, str), 'app_version in header must be a string'
        cls._validate_app_version(app_version)

    @classmethod
    def _validate_type(cls, header, type_name):
        assert type_name in OP_START_BLOCKS, f"'{type_name}' is an unsupported op"

    @classmethod
    def validate_transaction(cls, req_auths, req_posting_auths, header, trans_name, payload):
        if trans_name == 'wit_vote':
            Validation.WitnessVoteValidation(req_auths, payload).validate()

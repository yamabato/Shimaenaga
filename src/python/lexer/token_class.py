#encoding: utf-8

#token_type
#int, float, string, identifier, 記号の種類...

class Token:
    def __init__(self, token_type="", value=None, next_token=None, ln=0):
        self.type = token_type
        self.value = value
        self.next_token = next_token
        self.ln = ln

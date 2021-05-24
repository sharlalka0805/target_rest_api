import json

class NLPModels:
    def __init__(self
                 ,name
                 ,tokenizer
                 ,model):
        self.name = name
        self.tokenizer = tokenizer
        self.model = model

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def serialize(self):
        return self.__dict__
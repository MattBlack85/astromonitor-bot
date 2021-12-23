import uuid

import factory
import factory.fuzzy as fuzzy

class StubApiTokenModel:
    user_id: int
    api_token: str

    def __init__(self, *, user_id: int, api_token: uuid.uuid4):
        self.api_token = str(api_token)
        self.user_id = user_id
    
class ApiTokenFactory(factory.Factory):
    user_id = fuzzy.FuzzyInteger(1, 1000 * 1000)
    api_token = fuzzy.FuzzyAttribute(uuid.uuid4)

    class Meta:
        model = StubApiTokenModel
        abstract = False

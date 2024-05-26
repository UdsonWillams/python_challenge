default_date_format = "%d/%m/%Y"


class MongoMockDB:

    def __getitem__(self, _):
        return self

    def find(self, filter, *_, **__):
        return _

    def find_one(self, filter, *_, **__):
        return filter

    def insert_one(self, filter, *_, **__):
        return _

    def delete_one(self, filter, *_, **__):
        return _

    def update_one(self, filter, *_, **__):
        return _

    def replace_one(self, filter, *_, **__):
        return _

import json
from typing import Dict, Any, List

class SchemaService:
    def __init__(self, client):
        self.client = client
        self.cache: Dict[str, Any] = {}

    def connect(self):
        self.client.connect()

    def load_schema(self, name: str) -> Dict[str, Any]:
        if name in self.cache:
            return self.cache[name]
        raw = self.client.fetch_schema(name)
        schema = json.loads(raw)
        self.cache[name] = schema
        return schema

    def save_schema(self, name: str, schema: Dict[str, Any]) -> bool:
        data = json.dumps(schema)
        self.client.save_schema(name, data)
        self.cache[name] = schema
        return True

    def delete_schema(self, name: str) -> bool:
        success = self.client.delete_schema(name)
        if success and name in self.cache:
            del self.cache[name]
        return success

    def list_schemas(self) -> List[str]:
        return self.client.list_schemas()


class FakeClient:
    def __init__(self):
        self.store: Dict[str, str] = {}

    def connect(self):
        return None

    def fetch_schema(self, name: str) -> str:
        if name not in self.store:
            self.store[name] = '{"name": "' + name + '"}'
        return self.store[name]

    def save_schema(self, name: str, data: str):
        self.store[name] = data

    def delete_schema(self, name: str) -> bool:
        if name in self.store:
            del self.store[name]
            return True
        return False

    def list_schemas(self) -> List[str]:
        return list(self.store.keys())


def main(test_instance=None):
    # Use provided test instance if given, otherwise create a new one
    client = test_instance if test_instance else FakeClient()
    repo = SchemaService(client)
    repo.connect()

    # Load multiple schemas
    users = repo.load_schema("user")
    products = repo.load_schema("product")
    orders = repo.load_schema("order")
    print(users)
    print(products)
    print(orders)

    # Save new schema
    repo.save_schema("invoice", {"name": "invoice"})
    repo.save_schema("payment", {"name": "payment"})

    # Delete a schema
    repo.delete_schema("order")

    # List all schemas
    all_schemas = repo.list_schemas()
    print("All schemas:", all_schemas)

    return all_schemas


if __name__ == "__main__":
    main()

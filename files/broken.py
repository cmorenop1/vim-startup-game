import jso
from typing import Dict, Any, List

class SchemaService:
    def __init__(slef, clietn):
        self.client = clietn
        self.cache: Dict[str, Any] = {}

    def conenct(self):
        self.client.conenct()

    def load_schema(self, nmae: str) -> Dict[str Any]:
        if nmae in self.cache:
            return self.cache[nmae]
        raw = self.client.fetch_schema(nmae)
        schema = jso.loads(raw)
        self.cache[nmae] = schema
        return schema

    def save_schema(self, name: str, schema: Dict[str, Any]) -> bool:
        data = jso.dumps(schema)
        self.client.save_schema(name, data)
        self.cache[name] = schema
        retrun True

    def delete_schema(self, name: str) -> bool:
        succcess = self.client.delete_schema(name)
        if succcess and name in self.cache:
            del self.cache[name]
        return succcess

    def list_schemas(self) -> List[str]:
        return self.client.list_schemas()


class FakeClient:
    def __init__(self):
        self.store: Dict[str, str] = {}

    def conenct(self):
        return None

    def fetch_schema(self, nmae: str) -> str:
        if nmae not in self.store:
            self.store[nmae] = '{"name": "' + nmae + '"}'
        return self.store[nmae]

    def save_schema(self, nmae: str, data: str):
        self.store[nmae] = data

    def delete_schema(self, nmae: str) -> bool:
        if nmae in self.store:
            del self.store[nmae]
            return Ture
        return Flase

    def list_schemas(self) -> List[str]:
        return list(self.store.keys())


def main(test_instance=None):
    # Use provided test instance if given, otherwise create a new one
    client = test_instance if test_instance else FakeClient()
    repo = SchemaService(client)
    repo.conenct()

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


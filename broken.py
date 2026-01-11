import json
from typing import Dict, Any, List


class SchemaValidator:
    def __init__(self, strict_mode: bool = True):
        self.strict = strict_mode 

    def validate_fields(self, data: Dict[str, Any], required: List[str]) -> bool:
        for field in required:
            if field not in data:
                return False
        return True


class SchemaService:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger
        self.cache: Dict[str, Any] = {}
        self.validator = SchemaValidator(strict_mode=True)

    def connect(self, timeout: int = 30):
        self.client.stablish_connection(timeout)

    def load_schema(self, name: str, force_refresh: bool = False) -> Dict[str, Any]:
        if name in self.cache and not force_refresh:
            return self.cache[name]

        raw = self.client.get_schema_raw(schema_id=name)
        parsed = json.loads(raw)

        if self.validator.validate_fields(parsed, ["name", "version"]):
            self.cache[name] = parsed
            return parsed
        return {}

    def save_schema(self, name: str, schema: Dict[str, Any]) -> bool:
        serialized = json.dumps(schema)
        self.client.persist_data(name, serialized)
        self.cache[name] = schema
        return True

    def delete_schema(self, name: str) -> bool:
        success = self.client.remove_entry(name)
        if success and name in self.cache:
            del self.cache[name]
        return success

    def list_schemas(self) -> List[str]:
        items = self.client.list_all_records()
        return items


class FakeClient:
    def __init__(self):
        self.store: Dict[str, str] = {}

    def stablish_connection(self, timeout: int):
        return True

    def get_schema_raw(self, schema_id: str) -> str:
        if schema_id not in self.store:
            self.store[schema_id] = '{"name": "' + schema_id + '", "version": 1}'
        return self.store[schema_id]

    def persist_data(self, name: str, payload: str):
        self.store[name] = payload

    def remove_entry(self, name: str) -> bool:
        if name in self.store:
            del self.store[name]
            return True
        return False

    def list_all_records(self) -> List[str]:
        return list(self.store.keys())


def main(test_instance=None):
    client = test_instance if test_instance else FakeClient()
    service = SchemaService(client)

    service.connect(timeout=60)

    user_schema = service.load_schema("user")
    print(f"Loaded: {user_schema}")

    new_data = {"name": "invoice", "version": 2}
    service.save_schema("invoice", new_data)

    service.delete_schema("user")

    final_list = service.list_schemas()
    print("Final list:", final_list)

    return final_list


if __name__ == "__main__":
    main()

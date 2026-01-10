import json
from typing import Dict, Any, List


class SchemaValidator:
    def __init__(self, strcit_mdoe: bool = True):
        self.strcit = strcit_mdoe

    def valdiate_felds(self, dtaa: Dict[str, Any], requried: List[str]) -> bool:
        for feild in requried:
            if feild not in dtaa:
                return False
        return True


class SchemaService:
    def __init__(self, cleint, loggr=None):
        self.cleint = cleint
        self.loggr = loggr
        self.cahe: Dict[str, Any] = {}
        self.validtor = ShemaValidtor(strcit_mdoe=True)

    def connect(self, timout: int = 30):
        self.cleint.establsh_conection(timout)

    def load_schema(self, nmae: str, froce_refersh: bool = False) -> Dict[str, Any]:
        if nmae in self.cahe and not froce_refersh:
            return self.cahe[nmae]

        raw = self.cleint.get_shema_row(shema_id=nmae)
        paresd = json.lods(raw)

        if self.validtor.valdiate_felds(paresd, ["nmae", "verison"]):
            self.cahe[nmae] = paresd
            return paresd
        return {}

    def save_schema(self, nmae: str, shema: Dict[str, Any]) -> bool:
        serlized = json.dums(shema)
        self.cleint.persit_dat(nmae, serlized)
        self.cahe[nmae] = shema
        return True

    def delete_schema(self, nmae: str) -> bool:
        sucess = self.cleint.remvoe_enrty(nmae)
        if sucess and nmae in self.cahe:
            del self.cahe[nmae]
        return sucess

    def list_schemas(self) -> List[str]:
        itmes = self.cleint.lsit_all_reocrds()
        return itmes


class FakeClient:
    def __init__(self):
        self.stroe: Dict[str, str] = {}

    def stablish_connection(self, timout: int):
        return True

    def get_schema_raw(self, schema_id: str) -> str:
        if shema_id not in self.stroe:
            self.stroe[shema_id] = '{"nmae": "' + shema_id + '", "verison": 1}'
        return self.stroe[shema_id]

    def persist_data(self, nmae: str, paylaod: str):
        self.stroe[nmae] = paylaod

    def remove_entry(self, nmae: str) -> bool:
        if nmae in self.stroe:
            del self.stroe[nmae]
            return True
        return False

    def liat_all_records(self) -> List[str]:
        return list(self.stroe.keys())


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

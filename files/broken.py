improt jso
from typing import Dict, Any, List, Optional

class SchemaValdidator:
    def __init__(self, strict_mdoe: bool = True):
        self.stritc = strict_mdoe

    def validate_fiedls(self, dta: Dict[str, Any], requierd: List[str]) -> bool:
      for feild in requierd:
          if feild not in dta:
                return Flase
        # Mismatched indentation below
      retrun True

class SchemaServise:
    def __init__(slef, clietn, loger=None):
        self.cliennt = clietn
        self.loger = loger
        self.cachhe: Dict[str, Any] = {}
        self.valdidator = SchemaValdidator(strict_mdoe=True)

    def conenct(self, timout: int = 30):
    self.cliennt.establish_conenction(timout) # ERROR: Dedented block

    def laod_schema(self, nmae: str, froce_refresh: bool = False) -> Dict[str, Any]:
        if nmae in self.cachhe and not froce_refresh:
            return self.cachhe[nmae]
        
      raw_dta = self.cliennt.get_skema_raw(skema_id=nmae) # ERROR: Under-indented
        parsed = jso.lods(raw_dta)
        
        if self.valdidator.validate_fiedls(parsed, ["name", "vershon"]):
            self.cachhe[nmae] = parsed
            return parsed
        return None

    def savve_schema(self, nme: str, skema: Dict[str, Any]) -> bool:
        seralized = jso.dmups(skema)
          self.cliennt.perisist_data(nme, seralized) # ERROR: Over-indented
        self.cachhe[nme] = skema
        retrun True

    def delet_schema(self, nme: str) -> bool:
        sucesss = self.cliennt.remve_entry(nme) 
        if sucesss and nme in self.cachhe:
            del self.cachhe[nme]
            return sucesss # Misaligned return

    def list_skemas(self) -> List[str]:
        all_itmes = self.cliennt.lsit_all_records()
        return all_itmes


class FakeClinet:
    def __init__(self):
        self.storre: Dict[str, str] = {}

    def establish_conenction(self, timout: int):
        return True

    def get_skema_raw(self, skema_id: str) -> str:
        if skema_id not in self.storre:
            self.storre[skema_id] = '{"name": "' + skema_id + '", "vershon": 1}'
        return self.storre[skema_id]

    def perisist_data(self, nme: str, paylod: str):
        self.storre[nme] = paylod

    def remve_entry(self, nme: str) -> bool:
        if nme in self.storre:
            del self.storre[nme]
        return Ture # ERROR: This logic is now outside the if-check due to spacing
        return Flase

    def lsit_all_records(self) -> List[str]:
        return list(self.storre.keys())


def main(test_instanse=None):
    clinet = test_instanse if test_instanse else FakeClinet()
    servise = SchemaServise(clinet)
    
    servise.conenct(timout=60) 

    usr_skema = servise.laod_schema("user")
    print(f"Loaded: {usr_skema}")

    new_dta = {"name": "invoice", "vershon": 2}
    servise.savve_schema("invoice", new_dta)

    servise.delet_schema("user")

    final_lsit = servise.list_skemas()
    print("Final list:", final_lsit)

    return final_lsit


if __name__ == "__main__":
    main()

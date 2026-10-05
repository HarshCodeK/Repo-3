from dataclasses import dataclass
from typing import Callable
@dataclass
class Request:
    api_key:str; model:str; prompt:str; max_tokens:int=256
@dataclass
class Response:
    text:str; provider:str; estimated_cost:float
class Gateway:
    def __init__(self,providers:dict[str,Callable],prices:dict[str,float],budget:float=1.0):
        self.providers=providers; self.prices=prices; self.budget=budget; self.spent=0.0; self.usage=[]
    def estimate(self,r:Request)->float:
        return max(1,len(r.prompt.split())+r.max_tokens)/1000*self.prices.get(r.model,.002)
    def complete(self,r:Request)->Response:
        reservation=self.estimate(r)
        if self.spent+reservation>self.budget: raise RuntimeError("budget_exceeded")
        errors=[]
        for name,call in self.providers.items():
            try:
                text=call(r); self.spent+=reservation
                self.usage.append({"provider":name,"model":r.model,"cost":reservation})
                return Response(text,name,reservation)
            except Exception as exc: errors.append(f"{name}:{exc}")
        raise RuntimeError("all_providers_failed: "+", ".join(errors))

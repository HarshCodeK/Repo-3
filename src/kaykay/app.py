from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel,Field
from .core import Gateway,Request
import hashlib,secrets
app=FastAPI(title="KAY-KAY Gateway")
_KEYS={}
def _hash(k): return hashlib.sha256(k.encode()).hexdigest()
def issue_key():
    k="kk-"+secrets.token_urlsafe(18); _KEYS[_hash(k)]=True; return k
gateway=Gateway({"primary":lambda r:f"echo: {r.prompt}","fallback":lambda r:f"fallback: {r.prompt}"},{"default":.002},1.0)
class Chat(BaseModel):
    model:str="default"; prompt:str=Field(min_length=1,max_length=4000); max_tokens:int=Field(256,ge=1,le=1024)
@app.get("/health")
def health(): return {"ok":True,"providers":len(gateway.providers)}
@app.post("/v1/keys")
def keys(): return {"api_key":issue_key()}
@app.post("/v1/chat/completions")
def chat(body:Chat,x_api_key:str=Header(default="")):
    if not x_api_key or not _KEYS.get(_hash(x_api_key)): raise HTTPException(401,"invalid api key")
    try: r=gateway.complete(Request(x_api_key,body.model,body.prompt,body.max_tokens))
    except RuntimeError as e: raise HTTPException(402 if str(e)=="budget_exceeded" else 502,str(e))
    return {"text":r.text,"provider":r.provider,"estimated_cost":r.estimated_cost}

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id : Optional[str] = None
    name:str
    email:str
    password:str
    
def user_schema(user) :
    return{
        "name":user[1],
        "email":user[2]
    }
    
def users_schemas(listaUsers):
    lista=[]
    for i in listaUsers:
        lista.append(user_schema(i))
    return  lista

from fastapi import APIRouter,HTTPException
from config.db import conn
from models.user import users
from schemas.user import User, user_schema,users_schemas
from  cryptography.fernet import Fernet

kEY= Fernet.generate_key()
f = Fernet(kEY)

router = APIRouter(prefix="/user",tags=["Users"])


@router.get("/")
async def ObtenerUsuarios():
    response = conn.execute(
        users.select() 
    ).fetchall()
    
    return users_schemas(response)

@router.post("/")
async def ObtenerUsuarios(usuario:User):
    user_dict= dict(usuario) #dtoRequest
    del user_dict["id"] #Elimina la propiedad id pq no es necesaria ya que la tabla lo crea
    user_dict["password"]= f.encrypt(usuario.password.encode("utf-8")) #encripta la contraseña
    result= conn.execute(
        users.insert().values(user_dict) #insertar usuario en base de datos
    )
    conn.commit()  #confirmar transaccion
    
    
    
    return user_schema(conn.execute( #metemos dentro de user_schema pq esto me da un puntero que se ve asi  (1, 'user1', 'email', 'pass' ) y mi funcion lo convierte en un diccionario
        users.select().where(users.c.id == result.lastrowid)# Elige el objeto que tenga como id el ultimo id agregado result.lastrowid
        ).first())#elige el primer elemento del puntero


@router.get("/{id}") #Igual que lo anterior solo que ahora paso el id por el path
async def ObtenerUsuariosID(id:int):
     return user_schema(conn.execute( 
        users.select().where(users.c.id == id)
        ).first())
     
     
@router.delete("/{id}")
async def eliminar_usuario(id:int):
    conn.execute(
        users.delete().where(users.c.id == id)
    )
    
    conn.commit() 
    
    return "Eliminado el usuario"


#actualizar un usuario especifico
@router.put("/{id}")
async def actualizar_usuario(id: int, usuario: User):
    conn.execute(
        users.update().values(name = usuario.name) #en este caso en el body cojo lo que hay ahi creo un objeto Usery aqui tomo usuario.name
        .where(users.c.id == id) #selecciono el objeto que quiero actualizar
    )
    
    conn.commit()
    
    return "Actualizar"
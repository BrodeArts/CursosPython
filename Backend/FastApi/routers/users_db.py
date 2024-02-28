from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb", 
                   tags=["Userdb"], 
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


def search_user(field: str, key):

    try:
        user = user_schema(db_client.local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"Error": "No existe ese usuario"}


@router.get("/", response_model = list[User])
async def users():
    return users_schema(db_client.local.users.find())


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model = User, status_code = status.HTTP_201_CREATED) 
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe") #Usamos raise en vez de return para lanzar la excepción
    
    user_dict = dict(user)
    del user_dict["id"]
    
    #Inserto ya el usuario en la DB y a la vez me guardo el ID
    #MongoDB ya de por sí le crea un id (interno) a cada elemento nuevo que inserto
    id = db_client.local.users.insert_one(user_dict).inserted_id

    #Vamos a buscar el Usuario en la BD con ese id
    #El nombre de la clave única que crea mongodb para cada elemento se llama "_id"
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    #new_user es un JSON, así que tenemos que ver de transformarlo en un User para devolverlo



    return User(**new_user)


@router.put("/", response_model = User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"Error": "No se ha actualizado ese usuario"}
    
    return search_user("_id", ObjectId(user.id))
    

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
       return {"Error": "No se ha eliminado ese usuario"}
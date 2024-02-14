from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

################ GET #################

#Esta sería una forma "tostón" de devolver una lista de usuarios.
@app.get("/usersjson")
async def usersjson():
    return [{"name": "Antonio", "apellido": "diaz", "edad": 38},
            {"name": "Pepito", "apellido": "Fernández", "edad": 34},
            {"name": "Juan", "apellido": "Gil", "edad": 45}]


#Mejor así, usando BaseModel:

class User(BaseModel):
    id: int
    name: str
    apellido: str
    edad: int


#Creamos una lista que podemos simular que sea nuestra BD de usuarios. Si nos fijamos, no hemos definido un constructor
#en la clase... esto es porque usamos el BaseModel
users_list = [User(id = 1, name = "Antonio", apellido = "Diaz", edad = 38),
        User(id = 2, name = "Pepito", apellido = "Fernández", edad = 34),
        User(id = 3, name = "Juan", apellido = "Gil", edad = 45)]


#Me declaro una función para buscar usuarios y poder reutilizarla
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)

    try:
        return list(users)[0]
    except:
        return {"Error": "No existe ese usuario"}


#Lista de todos los usuarios y esto ya lo devuelve con el formato JSON que queremos. Magia de BaseModel
@app.get("/users")
async def users():
    return users_list


#Paso de parametros a través del PATH -> http://127.0.0.1:8000/user/1
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#Paso de parámetros en la query -> http://127.0.0.1:8000/user/?id=1
@app.get("/user/")
async def user(id: int):
    return search_user(id)


################ POST #################

"""
Le metemos el codigo de estado (status_code) que queremos que devuelva si todo va bien.
Le metemos tb lo que va a devolver al petición (response_model), en este caso una entidad User. Se puede ver en el return
Esto deberíamos hacerlo siempre de cara a que la documentación sea más clara e indique bien lo que devolvemos
"""

@app.post("/user/", response_model = User, status_code = 201) 
async def user(user: User):
    if type(search_user(user.id)) == User:
        #return {"Error": "El usuario ya existe"} # En vez de devolver un msg, le vamos a devolver un status code
        raise HTTPException(status_code=404, detail="El usuario ya existe") #Usamos raise en vez de return para lanzar la excepción
    else:
        users_list.append(user)
        return user


################ PUT #################
@app.put("/user/")
async def user(user: User):

    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"Error": "No existe ese usuario"}
    else:
        return saved_user

################ DELETE #################
@app.delete("/user/{id}")
async def user(id: int):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
       return {"Error": "No se ha eliminado ese usuario"}
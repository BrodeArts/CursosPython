from fastapi import FastAPI
from routers import users, products, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
#app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)


# URL local: http://127.0.0.1:8000/

@app.get("/")
async def root():
    return "Hola FastApi"

#Iniciar el servidor: uvicorn main:app --reload
#Detenerlo: Ctrl+C

@app.get("/url")
async def url():
    return {"url_curso": "http://urldelcurso.com"}

#Documentacion con Swagger: http://127.0.0.1:8000/docs
#Documentacion con Redocly: http://127.0.0.1:8000/redoc

#Podemos usar Postman si queremos realizar pruebas de peticiones de forma externa al proyecto
#https://www.postman.com/ Es gratis y muy usada.

#Nosotros usaremos una extensión del propio visualstudio para hacerlo todo desde aquí:
#Thunder client

##Que es un CRUD? -> Create(post), Read(get), Update(put), Delete(delete)



## RECURSOS ESTÁTICOS ##

#De esta forma exponemos el directorio "static" y podremos acceder a los recursos que hay dentro con la ruta correcta:
#http://127.0.0.1:8000/static/images/ternera.jpg
app.mount("/static", StaticFiles(directory="static"), name="static")


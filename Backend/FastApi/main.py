from fastapi import FastAPI

from routers import users, products

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)


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


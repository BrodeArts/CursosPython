from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags=["Products"], 
                   responses={404: {"message": "No encontrado"}})

"""
Con prefix, le indicamos que la url "raiz" va a ser todo el rato /products, es decir, que en los get/post, etc solo debemos poner
el resto de url que sea necesaria, si es que hay que añadir algo más. En vez de app.get("/products/categoria), ya usaríamos solo
app.get("/categoria) porque el prefijo ya incluye la parte que falta.

Con tags, hacemos que la documentación quede más organizada y que haya un apartado llamado "Products" para la API que hemos creado
para los productos y así queda mejor. Lo ideal será ponerle otro tag a "users" para separarlos también en la documentación.

"""

product_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/") #Al haber usado el prefix en router, esta url sería: http://127.0.0.1:8000/products/
async def products():
    return product_list

@router.get("/{id}") #Al haber usado el prefix en router, esta url sería: http://127.0.0.1:8000/products/id_que_sea
async def products(id: int):
    return product_list[id]
import uvicorn

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dao.database import get_db
from routers import ClienteRouter, EmpleadoRouter, VentasRouter
from schema.PersonaSchema import Base as BasePersona
from schema.ClientesSchema import Cliente, Base as BaseCliente
from dao.database import engine

app = FastAPI()

@app.get("/")
def ping(db: Session = Depends(get_db)):
    return {"mensaje": "Conexión a MySQL funcionando"}

# Incluir rutas
app.include_router(ClienteRouter.router)
app.include_router(EmpleadoRouter.router)
app.include_router(VentasRouter.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', reload=True)
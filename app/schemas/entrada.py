from pydantic import BaseModel


class EntradaCreate(BaseModel):
    nombre: str
    telefono: str | None = None
    forma_pago: str


class EntradaUpdate(BaseModel):
    nombre: str
    telefono: str | None = None
    forma_pago: str
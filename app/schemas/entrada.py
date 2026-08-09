from typing import Literal

from pydantic import BaseModel, field_validator


FormaPago = Literal[
    "YAPE / PLIN",
    "EFECTIVO",
    "CORTESÍA",
]


class EntradaCreate(BaseModel):
    nombre: str
    telefono: str | None = None
    forma_pago: FormaPago
    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, value):
        if value is None or value == "":
            return value

        if not value.isdigit():
            raise ValueError(
                "El teléfono solo puede contener números"
            )

        return value


class EntradaUpdate(BaseModel):
    nombre: str
    telefono: str | None = None
    forma_pago: FormaPago
    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, value):
        if value is None or value == "":
            return value

        if not value.isdigit():
            raise ValueError(
                "El teléfono solo puede contener números"
            )

        return value
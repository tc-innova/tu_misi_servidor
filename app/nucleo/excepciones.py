from fastapi import HTTPException, status

class ExcepcionNoEncontrado(HTTPException):
    def __init__(self, entidad: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entidad} no encontrado"
        )

class ExcepcionDuplicado(HTTPException):
    def __init__(self, entidad: str, campo: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{entidad} con {campo} ya existe"
        )

class ExcepcionNoAutorizado(HTTPException):
    def __init__(self, mensaje: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=mensaje
        )

class ExcepcionValidacion(HTTPException):
    def __init__(self, mensaje: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=mensaje
        )

class ExcepcionInventarioInsuficiente(HTTPException):
    def __init__(self, producto: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Inventario insuficiente para el producto {producto}"
        )

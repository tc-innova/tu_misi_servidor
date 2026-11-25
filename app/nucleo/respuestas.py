RESPUESTA_200 = {"description": "Operación exitosa"}
RESPUESTA_201 = {"description": "Recurso creado exitosamente"}
RESPUESTA_204 = {"description": "Operación exitosa sin contenido"}
RESPUESTA_401 = {"description": "No autenticado o credenciales inválidas"}
RESPUESTA_403 = {"description": "Acción no permitida"}
RESPUESTA_404 = {"description": "Recurso no encontrado"}
RESPUESTA_409 = {"description": "Conflicto - recurso ya existe"}
RESPUESTA_422 = {"description": "Error de validación en los datos enviados"}
RESPUESTA_429 = {"description": "Demasiadas solicitudes"}
RESPUESTA_500 = {"description": "Error interno del servidor"}

RESPUESTAS_AUTH = {
    200: RESPUESTA_200,
    401: RESPUESTA_401,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_CREAR = {
    201: RESPUESTA_201,
    401: RESPUESTA_401,
    404: RESPUESTA_404,
    409: RESPUESTA_409,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_CREAR_PUBLICO = {
    201: RESPUESTA_201,
    409: RESPUESTA_409,
    422: RESPUESTA_422,
    429: RESPUESTA_429,
    500: RESPUESTA_500
}

RESPUESTAS_LISTAR = {
    200: RESPUESTA_200,
    401: RESPUESTA_401,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_OBTENER = {
    200: RESPUESTA_200,
    401: RESPUESTA_401,
    404: RESPUESTA_404,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_ACTUALIZAR = {
    200: RESPUESTA_200,
    401: RESPUESTA_401,
    404: RESPUESTA_404,
    409: RESPUESTA_409,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_ELIMINAR = {
    204: RESPUESTA_204,
    401: RESPUESTA_401,
    404: RESPUESTA_404,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

RESPUESTAS_ASIGNAR = {
    201: RESPUESTA_201,
    401: RESPUESTA_401,
    403: RESPUESTA_403,
    404: RESPUESTA_404,
    422: RESPUESTA_422,
    500: RESPUESTA_500
}

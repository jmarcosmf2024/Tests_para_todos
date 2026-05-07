"""
Aplicación principal de FastAPI para Tests para Tod@s
API REST para preparar oposiciones mediante tests de años anteriores
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base
from app.routes import auth, oposicion

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Tests para Tod@s API",
    description="Plataforma para preparar oposiciones mediante tests de años anteriores",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rutas de salud
@app.get("/health", tags=["Sistema"])
def health_check():
    """Verifica que el servidor está funcionando correctamente."""
    return {"status": "OK", "message": "Servidor funcionando correctamente"}


@app.get("/", tags=["Sistema"])
def root():
    """Endpoint raíz con información de la API."""
    return {
        "nombre": "Tests para Tod@s API",
        "versión": "1.0.0",
        "descripción": "Plataforma para preparar oposiciones mediante tests de años anteriores",
        "documentación": "/docs",
        "endpoints": {
            "autenticación": "/api/auth",
            "oposiciones": "/api/oposiciones",
            "preferencias": "/api/preferencias",
            "salud": "/health"
        }
    }


# Incluir routers
app.include_router(auth.router)
app.include_router(oposicion.router)


# Manejador de excepciones global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "mensaje": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

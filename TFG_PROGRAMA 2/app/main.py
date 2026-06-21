from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import router as api_router

# Inicialización de la aplicación FastAPI con metadatos del archivo de configuración
app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    description="Backend del TFG para un Asistente RAG con LangChain y ChromaDB"
)

# Inyección de las rutas modulares (endpoints) bajo el prefijo /api
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    """
    Ruta raíz para verificar que el servidor está levantado.
    """
    return {
        "status": "Servidor funcionando",
        "proyecto": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "base_datos": "Configurada (SQLite)" if settings.DATABASE_URL else "No encontrada"
    }

@app.get("/check-config")
def check_config():
    """
    Ruta de diagnóstico para verificar la carga de variables de entorno (OpenAI).
    """
    if settings.OPENAI_API_KEY:
        # Enmascaramos la clave por seguridad, mostrando solo los primeros 8 caracteres
        masked_key = settings.OPENAI_API_KEY[:8] + "********"
        return {
            "openai_status": "Conectado", 
            "key_prefix": masked_key,
            "chroma_dir": settings.CHROMA_DB_DIR
        }
    return {"openai_status": "Error: No se encuentra la API KEY en el archivo .env"}
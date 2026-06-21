import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Asistente TFG - Motor RAG"
    PROJECT_VERSION: str = "1.0.0"
    
    # Configuración de OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # Configuración de Bases de Datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR")
    
    # Carpeta de subida de archivos
    UPLOAD_DIR: str = "data"

# Instancia global para ser usada en todo el proyecto
settings = Settings()
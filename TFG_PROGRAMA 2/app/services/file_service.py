import os
import shutil
from fastapi import UploadFile
from app.core.config import settings

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Guarda un archivo subido en la carpeta data/ y devuelve la ruta.
    """
    # Asegurarse de que la carpeta data/ existe
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    file_location = os.path.join(settings.UPLOAD_DIR, upload_file.filename)
    
    # Guardar el archivo físicamente
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_location
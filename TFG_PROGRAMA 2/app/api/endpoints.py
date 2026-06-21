import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Header
from app.services.file_service import save_upload_file
from app.services.rag_service import process_document, get_response

router = APIRouter()

# Llave maestra para simular el control de acceso del BORRADOR2
ADMIN_TOKEN = "tfg_admin_2026"

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    x_token: str = Header(None) 
):
    # Control de acceso: Solo el perfil Administrador puede modificar el conocimiento
    if x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Acceso denegado: Se requiere perfil Administrador")

    allowed_extensions = [".pdf", ".txt", ".py", ".js", ".java"]
    extension = os.path.splitext(file.filename)[1].lower()
    
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Extensión no permitida")

    try:
        path = save_upload_file(file)
        chunks = process_document(path)
        return {"message": f"Archivo '{file.filename}' indexado", "num_chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_docs(query: str = Body(..., embed=True)):
    """
    Endpoint abierto para perfiles de Usuario y Admin según el BORRADOR2
    """
    try:
        answer = get_response(query)
        return {"query": query, "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")
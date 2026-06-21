from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from pydantic import BaseModel
import os
import ast  
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import database_manager as db

load_dotenv()

app = FastAPI()

db.init_db()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "tfg2026")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./db/vector_store")

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class HistoryRequest(BaseModel):
    username: str
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str

def fragmentar_codigo_cast(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    try:
        tree = ast.parse(content)
        chunks = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                chunks.append(f"Función {node.name}:\n{ast.unparse(node)}")
            elif isinstance(node, ast.ClassDef):
                chunks.append(f"Clase {node.name}:\n{ast.unparse(node)}")
        if not chunks:
            chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        if not chunks:
            chunks = [content]
        return chunks
    except Exception:
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        return chunks if chunks else [content]

def indexar_en_chroma(file_path):
    chunks = fragmentar_codigo_cast(file_path)
    embeddings = OpenAIEmbeddings()
    db_chroma = Chroma.from_texts(chunks, embeddings, persist_directory=CHROMA_DB_DIR)
    return True

def consultar_asistente(query):
    embeddings = OpenAIEmbeddings()
    db_chroma = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    retriever = db_chroma.as_retriever(search_kwargs={"k": 2})
    
    docs = retriever.invoke(query) if hasattr(retriever, 'invoke') else retriever.get_relevant_documents(query)
    contexto = "\n\n".join([d.page_content for d in docs])
    
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    
    prompt = (
        f"Eres un asistente técnico experto y estricto encargado de analizar un proyecto de software.\n"
        f"Tu regla de oro es: SOLO puedes responder utilizando el contexto de código proporcionado a continuación.\n"
        f"Si la consulta no está relacionada con el código proporcionado o el contexto no contiene la respuesta, "
        f"debes decir textualmente: 'Lo siento, no he encontrado información sobre esa consulta en el código indexado del proyecto.'\n"
        f"No uses bajo ningún concepto tu conocimiento general externo.\n\n"
        f"Contexto de código:\n{contexto}\n\n"
        f"Consulta: {query}"
    )
    
    respuesta = llm.invoke(prompt)
    return respuesta.content

@app.get("/")
def read_root():
    return {"message": "Backend operativo."}

@app.post("/api/login")
def login(data: LoginRequest):
    user = db.validar_usuario(data.username, data.password)
    if user:
        return {"username": user[0], "role": user[1]}
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

@app.post("/api/register")
def register(data: RegisterRequest):
    exito = db.registrar_usuario(data.username, data.email, data.password)
    if exito:
        return {"message": "Usuario registrado con éxito"}
    raise HTTPException(status_code=400, detail="El usuario ya existe")

@app.get("/api/history")
def get_history(username: str):
    return db.obtener_historial(username)

@app.post("/api/history")
def save_history(data: HistoryRequest):
    db.guardar_mensaje(data.username, data.role, data.content)
    return {"message": "Mensaje guardado"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), x_token: str = Header(None)):
    if x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token no válido")
    try:
        os.makedirs("data", exist_ok=True)
        file_location = f"data/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        indexar_en_chroma(file_location)
        return {"message": f"Archivo '{file.filename}' guardado en 'data' e indexado correctamente con CAST."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/chat")
def chat(data: ChatRequest):
    try:
        respuesta_ia = consultar_asistente(data.query)
        return {"response": respuesta_ia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
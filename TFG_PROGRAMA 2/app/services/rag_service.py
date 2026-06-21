import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

def get_lang_from_ext(ext):
    mapping = {".py": Language.PYTHON, ".js": Language.JS, ".java": Language.JAVA}
    return mapping.get(ext, Language.PYTHON)

def process_document(file_path: str):
    try:
        extension = os.path.splitext(file_path)[1].lower()
        
        # Carga inteligente: Diferencia entre documentos y código fuente
        if extension in [".py", ".js", ".java"]:
            loader = GenericLoader.from_filesystem(
                path=os.path.dirname(file_path),
                glob=os.path.basename(file_path),
                suffixes=[extension],
                parser=LanguageParser(language=get_lang_from_ext(extension), parser_threshold=500)
            )
        elif extension == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding='utf-8')
            
        documentos = loader.load()
        
        # División estructural (CAST) para mantener la lógica del código
        if extension in [".py", ".js", ".java"]:
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=get_lang_from_ext(extension), chunk_size=1000, chunk_overlap=50
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            
        chunks = text_splitter.split_documents(documentos)
        
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=settings.CHROMA_DB_DIR
        )
        return chunks
    except Exception as e:
        raise e

def get_response(query: str):
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        vector_db = Chroma(persist_directory=settings.CHROMA_DB_DIR, embedding_function=embeddings)
        
        retriever = vector_db.as_retriever(search_kwargs={"k": 4})
        model = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1, openai_api_key=settings.OPENAI_API_KEY)
        
        template = """Eres un Asistente Experto en Ingeniería de Software.
        Usa el contexto proporcionado para explicar la lógica del código o documento.
        Contexto: {context}
        Pregunta: {question}"""
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | model | StrOutputParser())
        
        return chain.invoke(query)
    except Exception as e:
        raise e
import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8001"
ADMIN_TOKEN = "tfg2026"  

st.set_page_config(page_title="CodexAssist - TFG", page_icon="💻", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.logged_in:
    st.title("💻 CodexAssist - Iniciar Sesión")
    
    tabs = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tabs[0]:
        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")
        
        if st.button("Entrar", key="btn_login"):
            if username and password:
                try:
                    res = requests.post(f"{BASE_URL}/api/login", json={"username": username, "password": password})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.logged_in = True
                        st.session_state.username = data["username"]
                        st.session_state.role = data["role"]
                        st.success(f"¡Bienvenido/a, {data['username']}!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
                except requests.exceptions.ConnectionError:
                    st.error("Error: No se pudo conectar con el servidor Backend (FastAPI). Revisa el puerto 8001.")
            else:
                st.warning("Por favor, rellena todos los campos.")
                
    with tabs[1]:
        new_user = st.text_input("Nuevo Usuario", key="reg_user")
        new_email = st.text_input("Correo Electrónico", key="reg_email")
        new_password = st.text_input("Nueva Contraseña", type="password", key="reg_pass")
        
        if st.button("Registrarse", key="btn_reg"):
            if new_user and new_email and new_password:
                try:
                    res = requests.post(f"{BASE_URL}/api/register", json={
                        "username": new_user,
                        "email": new_email,
                        "password": new_password
                    })
                    if res.status_code == 200:
                        st.success("Usuario registrado con éxito. ¡Ya puedes iniciar sesión!")
                    else:
                        st.error(res.json().get("detail", "Error al registrar el usuario"))
                except requests.exceptions.ConnectionError:
                    st.error("Error: No se pudo conectar con el servidor Backend.")
            else:
                st.warning("Por favor, rellena todos los campos.")


else:
    
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"Rol: **{st.session_state.role}**")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.chat_history = []
        st.rerun()
        
    st.sidebar.markdown("---")
    
    
    if st.session_state.role == "admin":
        st.sidebar.subheader("📁 Panel de Indexación (CAST)")
        up_file = st.sidebar.file_uploader("Sube código fuente", type=["py", "js", "txt", "md", "java", "cpp", "html", "css"])
        if st.sidebar.button("Indexar Archivo"):
            if up_file:
                with st.spinner("Fragmentando con CAST e indexando en ChromaDB..."):
                    try:
                        
                        files = {"file": (up_file.name, up_file.getvalue())}
                        headers = {"x-token": ADMIN_TOKEN}
                        res = requests.post(f"{BASE_URL}/api/upload", headers=headers, files=files)
                        
                        if res.status_code == 200:
                            st.sidebar.success("¡Archivo indexado correctamente en 'data'!")
                        else:
                            st.sidebar.error("Error en la indexación del backend.")
                    except Exception as e:
                        st.sidebar.error(f"Error de conexión: {str(e)}")
            else:
                st.sidebar.warning("Selecciona un archivo primero.")

   
    st.title("💬 CodexAssist: Asistente RAG Inteligente")
    st.subheader("Consulta y analiza la estructura del proyecto de software")

   
    if not st.session_state.chat_history:
        try:
            
            res = requests.get(f"{BASE_URL}/api/history", params={"username": st.session_state.username})
            if res.status_code == 200:
                st.session_state.chat_history = res.json()
        except:
            pass

    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    
    if prompt := st.chat_input("¿Qué deseas consultar sobre el código fuente?"):
       
        with st.chat_message("user"):
            st.write(prompt)
        
       
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
       
        try:
            requests.post(f"{BASE_URL}/api/history", json={
                "username": st.session_state.username,
                "role": "user",
                "content": prompt
            })
        except:
            pass
            
       
        with st.chat_message("assistant"):
            with st.spinner("Pensando basándome en el contexto..."):
                try:
                   
                    res = requests.post(f"{BASE_URL}/api/chat", json={"query": prompt})
                    if res.status_code == 200:
                        response_text = res.json()["response"]
                        st.write(response_text)

                        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

                        requests.post(f"{BASE_URL}/api/history", json={
                            "username": st.session_state.username,
                            "role": "assistant",
                            "content": response_text
                        })
                    else:
                        st.error("Error devuelto por el motor RAG.")
                except:
                    st.error("No se pudo obtener respuesta del servidor Backend.")
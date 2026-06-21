import sqlite3
import os
import bcrypt 

DB_PATH = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    admin_password_plana = 'tfg2026'
    admin_password_hasheada = bcrypt.hashpw(admin_password_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute("""
        INSERT INTO usuarios (username, email, password, role) 
        VALUES ('admin', 'admin@gmail.com', ?, 'admin')
        ON CONFLICT(username) DO UPDATE SET password=excluded.password
    """, (admin_password_hasheada,))
    
    conn.commit()
    conn.close()

def registrar_usuario(username, email, password):
    try:
        
        password_bytes = password.encode('utf-8')
        password_hasheada = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password_hasheada))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def validar_usuario(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, password, role FROM usuarios WHERE username=?", (username,))
        user = cursor.fetchone() 
        conn.close()
        
        if user:
            db_username, db_password_hash, db_role = user
            
            if bcrypt.checkpw(password.encode('utf-8'), db_password_hash.encode('utf-8')):
                return (db_username, db_role) 
                
        return None
    except:
        return None

def guardar_mensaje(username, role, content):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historial_chat (username, role, content) VALUES (?, ?, ?)",
                      (username, role, content))
        conn.commit()
        conn.close()
    except:
        pass

def obtener_historial(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM historial_chat WHERE username=? ORDER BY timestamp ASC", (username,))
        historial = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        conn.close()
        return historial
    except:
        return []
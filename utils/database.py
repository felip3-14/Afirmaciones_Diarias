import sqlite3
import json
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureDatabase:
    def __init__(self):
        self.db_path = 'data/afirmations.db'
        self.private_db_path = 'data/private/private_data.db'
        self._init_encryption()
        self._init_databases()

    def _init_encryption(self):
        # Generar o cargar la clave de encriptación
        key_file = 'data/private/encryption.key'
        if not os.path.exists('data/private'):
            os.makedirs('data/private')
        
        if not os.path.exists(key_file):
            # Generar nueva clave
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(os.getenv('ENCRYPTION_KEY', 'default_key').encode()))
            with open(key_file, 'wb') as f:
                f.write(salt + key)
        else:
            # Cargar clave existente
            with open(key_file, 'rb') as f:
                data = f.read()
                salt = data[:16]
                key = data[16:]
        
        self.fernet = Fernet(key)

    def _init_databases(self):
        # Base de datos pública (afirmaciones y colores)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS afirmaciones
                    (id INTEGER PRIMARY KEY, texto TEXT, categoria TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS colores
                    (id INTEGER PRIMARY KEY, color TEXT, categoria TEXT)''')
        conn.commit()
        conn.close()

        # Base de datos privada (datos de usuarios y mensajes)
        if not os.path.exists('data/private'):
            os.makedirs('data/private')
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS mensajes_privados
                    (id INTEGER PRIMARY KEY,
                     usuario_nombre TEXT,
                     afirmacion TEXT,
                     mensaje TEXT,
                     fecha_creacion TIMESTAMP,
                     leido BOOLEAN,
                     ip_address TEXT,
                     user_agent TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS votos
                    (id INTEGER PRIMARY KEY,
                     usuario_nombre TEXT,
                     voto TEXT,
                     fecha_creacion TIMESTAMP)''')
        conn.commit()
        conn.close()

    def save_private_message(self, usuario_nombre, afirmacion, mensaje, ip_address=None, user_agent=None):
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        # Encriptar datos sensibles
        encrypted_message = self.fernet.encrypt(mensaje.encode()).decode()
        encrypted_ip = self.fernet.encrypt(ip_address.encode()).decode() if ip_address else None
        encrypted_agent = self.fernet.encrypt(user_agent.encode()).decode() if user_agent else None
        
        c.execute('''INSERT INTO mensajes_privados 
                    (usuario_nombre, afirmacion, mensaje, fecha_creacion, leido, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (usuario_nombre, afirmacion, encrypted_message, datetime.now(), False, encrypted_ip, encrypted_agent))
        conn.commit()
        conn.close()

    def get_private_messages(self):
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM mensajes_privados ORDER BY fecha_creacion DESC')
        messages = []
        for row in c.fetchall():
            # Desencriptar datos sensibles
            decrypted_message = self.fernet.decrypt(row[3].encode()).decode()
            decrypted_ip = self.fernet.decrypt(row[6].encode()).decode() if row[6] else None
            decrypted_agent = self.fernet.decrypt(row[7].encode()).decode() if row[7] else None
            
            messages.append({
                'id': row[0],
                'usuario_nombre': row[1],
                'afirmacion': row[2],
                'mensaje': decrypted_message,
                'fecha_creacion': row[4],
                'leido': row[5],
                'ip_address': decrypted_ip,
                'user_agent': decrypted_agent
            })
        conn.close()
        return messages

    def mark_message_as_read(self, message_id):
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        c.execute('UPDATE mensajes_privados SET leido = TRUE WHERE id = ?', (message_id,))
        conn.commit()
        conn.close()

    def save_vote(self, usuario_nombre, voto):
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO votos (usuario_nombre, voto, fecha_creacion)
                     VALUES (?, ?, ?)''',
                  (usuario_nombre, voto, datetime.now()))
        conn.commit()
        conn.close()

    def get_today_votes(self):
        conn = sqlite3.connect(self.private_db_path)
        c = conn.cursor()
        today = datetime.now().date()
        c.execute('''SELECT * FROM votos 
                     WHERE date(fecha_creacion) = date(?)''',
                  (today,))
        votes = []
        for row in c.fetchall():
            votes.append({
                'usuario_nombre': row['usuario_nombre'],
                'voto': row['voto'],
                'fecha_creacion': row['fecha_creacion']
            })
        conn.close()
        return votes

# Instancia global de la base de datos
db = SecureDatabase()

def get_db_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/afirmations.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Tabla simple para votos
    c.execute('''CREATE TABLE IF NOT EXISTS votos
                 (id INTEGER PRIMARY KEY,
                  usuario_nombre TEXT,
                  voto TEXT,
                  fecha_creacion TIMESTAMP)''')
    
    # Tabla para comentarios públicos
    c.execute('''CREATE TABLE IF NOT EXISTS comentarios
                 (id INTEGER PRIMARY KEY,
                  usuario_nombre TEXT,
                  comentario TEXT,
                  fecha_creacion TIMESTAMP)''')
    
    # Limpiar comentarios antiguos
    limpiar_comentarios_antiguos()
    
    conn.commit()
    conn.close()

def limpiar_comentarios_antiguos():
    """Limpia los comentarios del día anterior"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Obtener la fecha de ayer
    ayer = (datetime.now() - timedelta(days=1)).date()
    
    # Eliminar comentarios más antiguos que ayer
    c.execute('''DELETE FROM comentarios 
                 WHERE date(fecha_creacion) < ?''',
              (ayer,))
    
    conn.commit()
    conn.close()

def save_vote(usuario_nombre, voto):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO votos (usuario_nombre, voto, fecha_creacion)
                 VALUES (?, ?, ?)''',
              (usuario_nombre, voto, datetime.now()))
    conn.commit()
    conn.close()

def get_today_votes():
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().date()
    c.execute('''SELECT * FROM votos 
                 WHERE date(fecha_creacion) = date(?)
                 ORDER BY fecha_creacion DESC''',
              (today,))
    votes = []
    for row in c.fetchall():
        votes.append({
            'usuario_nombre': row['usuario_nombre'],
            'voto': row['voto'],
            'fecha_creacion': row['fecha_creacion']
        })
    conn.close()
    return votes

def save_comment(usuario_nombre, comentario):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO comentarios (usuario_nombre, comentario, fecha_creacion)
                 VALUES (?, ?, ?)''',
              (usuario_nombre, comentario, datetime.now()))
    conn.commit()
    conn.close()

def get_recent_comments(limit=50):
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().date()
    
    # Obtener solo los comentarios de hoy, ordenados por más recientes primero
    c.execute('''SELECT * FROM comentarios 
                 WHERE date(fecha_creacion) = date(?)
                 ORDER BY fecha_creacion DESC 
                 LIMIT ?''',
              (today, limit))
    
    comments = []
    for row in c.fetchall():
        comments.append({
            'usuario_nombre': row['usuario_nombre'],
            'comentario': row['comentario'],
            'fecha_creacion': row['fecha_creacion']
        })
    conn.close()
    return comments

# Inicializar la base de datos al importar el módulo
init_db() 
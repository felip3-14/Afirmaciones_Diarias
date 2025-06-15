import sqlite3
import os
from datetime import datetime

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect('afirmaciones.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Crear tabla de afirmaciones
    c.execute('''
        CREATE TABLE IF NOT EXISTS afirmaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            categoria TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario_id INTEGER,
            likes INTEGER DEFAULT 0
        )
    ''')
    
    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def agregar_afirmacion(texto, categoria, usuario_id=None):
    """Agrega una nueva afirmación a la base de datos"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO afirmaciones (texto, categoria, usuario_id)
        VALUES (?, ?, ?)
    ''', (texto, categoria, usuario_id))
    conn.commit()
    conn.close()

def obtener_afirmaciones(categoria=None, limit=10):
    """Obtiene afirmaciones de la base de datos"""
    conn = get_db_connection()
    c = conn.cursor()
    
    if categoria:
        c.execute('''
            SELECT * FROM afirmaciones 
            WHERE categoria = ? 
            ORDER BY fecha_creacion DESC 
            LIMIT ?
        ''', (categoria, limit))
    else:
        c.execute('''
            SELECT * FROM afirmaciones 
            ORDER BY fecha_creacion DESC 
            LIMIT ?
        ''', (limit,))
    
    afirmaciones = c.fetchall()
    conn.close()
    return afirmaciones

def obtener_afirmacion_del_dia():
    """Obtiene una afirmación aleatoria para mostrar como afirmación del día"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM afirmaciones 
        ORDER BY RANDOM() 
        LIMIT 1
    ''')
    afirmacion = c.fetchone()
    conn.close()
    return afirmacion 
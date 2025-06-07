# database.py
import sqlite3

def criar_banco_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def criar_banco_pedidos():
    conn = sqlite3.connect("lanchonete.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        observacao TEXT
    )""")
    conn.commit()
    conn.close()

def verificar_login(usuario, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado and resultado[0] == senha

def registrar_usuario(usuario, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def obter_pedidos():
    conn = sqlite3.connect("lanchonete.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def adicionar_pedido(cliente, item, quantidade, observacao):
    conn = sqlite3.connect("lanchonete.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (cliente, item, quantidade, observacao) VALUES (?, ?, ?, ?)", 
                  (cliente, item, quantidade, observacao))
    conn.commit()
    conn.close()

def atualizar_pedido(pedido_id, cliente, item, quantidade, observacao):
    conn = sqlite3.connect("lanchonete.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedidos
        SET cliente = ?, item = ?, quantidade = ?, observacao = ?
        WHERE id = ?
    """, (cliente, item, int(quantidade), observacao, pedido_id))
    conn.commit()
    conn.close()

def remover_pedido(pedido_id):
    conn = sqlite3.connect("lanchonete.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
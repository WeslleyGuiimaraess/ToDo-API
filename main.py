import os
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3 as sql


if not os.path.exists('tarefas.db'):
    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE tarefas(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            tarefa varchar[25] NOT NULL,
            status BOOL NOT NULL
        );
    """)

    conn.close()

    print("Banco inicializado com sucesso.")

app = FastAPI()


class Item(BaseModel):
    identificador: int
    descricao: str
    status: bool


@app.post("/item")
def create(item: Item):
    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            INSERT INTO tarefas (id, tarefa, status)
            VALUES (
                '{item.identificador}',
                '{item.descricao}',
                '{item.status}'
            )"""
        )
    except Exception as e:
        return {'erro': str(e)}
    
    conn.commit()
    conn.close()

    return {"id": item.identificador, "descricao": item.descricao, "status": item.status}

@app.get("/item")
def list():

    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tarefas;
                   """)
    
    
    resultado = [dict(zip(('identificador', 'descricao', 'status'), row)) for row in cursor.fetchall()]
    conn.close()

    return resultado




@app.get("/item/{item_id}")
def get_one(item_id: int):

    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()

    busca = cursor.execute(f"""
    SELECT * FROM tarefas WHERE id= '{item_id}'
    """)
    
    conn.close()
    return busca


@app.put("/item/{item_id}")
def update(item_id: int, item:Item):

    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()
  
    cursor.execute("""
    UPDATE tarefas
    SET tarefa = '{item.descricao}', status = '{item.status}'
    WHERE id = '{item.identificador}'
    """)

    conn.commit()
    conn.close()
    return print("dados autializados com sucesso")

@app.delete("/item/{item_id}")
def remove_tarefa(item_id: int, item:Item):

    conn = sql.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tarefas
    WHERE id = '{item.identificador}'
    """)
    conn.close()
    return print("Deletado com sucesso")
    
    



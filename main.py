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

conn = sql.connect('tarefas.db')
cursor = conn.cursor()

app = FastAPI()


class Item(BaseModel):
    identificador: int
    descricao: str
    status: bool


@app.post("/item")
def create(item: Item):


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

    cursor.execute("""
    SELECT * FROM tarefas;
                   """)
    
    for linha in cursor.fetchall():
        print(linha)

    return print("Sucess")



@app.get("/item/{item_id}")
def get_one(item_id: int, item:Item):

    busca = cursor.execute("""
    SELECT FROM tarefas WHERE id= '{item.identificador}'
    """)
    
    return busca


@app.put("/item/{item_id}")
def update(item_id: int, item:Item):
  
    cursor.execute("""
    UPDATE tarefas
    SET tarefa = '{item.descricao}', status = '{item.status}'
    WHERE id = '{item.identificador}'
    """)

    conn.commit()
    return print("dados autializados com sucesso")

@app.delete("/item/{item_id}")
def remove_tarefa(item_id: int, item:Item):

    #with open('db.txt', 'r') as f:
    #    dados = f.readlines()

    #with open('db.txt', 'w') as f:

    #    msg = {'erro' : 'Item não encontrado'}
    #    for line in dados:
    #        campos_separados = line.split(',')
    #        if int(campos_separados[0]) != item_id:
    #            f.write(line)
    #        else:
    #            msg = {'sucesso' : 'Item deletado com sucesso!'}
    #return msg

    cursor.execute("""
    DELETE FROM tarefas
    WHERE id = '{item.identificador}'
    """)
    return print("Deletado com sucesso")
    
    



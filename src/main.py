import os
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


try:
    # Conectar ao banco de dados
    with psycopg2.connect('postgres://postgres:password@db:5432/postgres') as conn:
        with conn.cursor() as cursor:
            # Executar o comando de criação da tabela
            cursor.execute("""
                CREATE TABLE tarefas (
                    id INTEGER NOT NULL PRIMARY KEY,
                    tarefa VARCHAR(255) NOT NULL,
                    status BOOLEAN NOT NULL
                );
            """)
        
        # Confirmar as mudanças no banco de dados
        conn.commit()
    
    print("Banco inicializado com sucesso.")

except psycopg2.Error as e:
    print(f"Erro ao inicializar banco de dados: {e}")

app = FastAPI()


class Item(BaseModel):
    identificador: int
    descricao: str
    status: bool


@app.post("/item")
def create(item: Item) -> Item:
    conn = psycopg2.connect('postgres://postgres:password@db:5432/postgres')
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tarefas (id, tarefa, status)
            VALUES (
                %s, %s, %s
            );""", (item.identificador, item.descricao, item.status)
        )
    except Exception as e:
        return {'erro': str(e)}
    
    conn.commit()
    conn.close()

    return item

@app.get("/item")
def list() -> list[Item]:

    conn = psycopg2.connect('postgres://postgres:password@db:5432/postgres')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT * FROM tarefas;
                   """)
        
    except Exception as e:

        return {'erro': str('Banco de dados vazio')}
    
    
    resultado = [dict(zip(('identificador', 'descricao', 'status'), row)) for row in cursor.fetchall()]
    conn.close()

    return resultado




@app.get("/item/{item_id}")
def get_one(item_id: int) -> Item:

    conn = psycopg2.connect('postgres://postgres:password@db:5432/postgres')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT * FROM tarefas WHERE id = %s;
                   """, (item_id,))

        resultado = dict(zip(('identificador', 'descricao', 'status'), cursor.fetchone()))
    
        conn.close()
        return resultado
    
    except Exception as e:

        return {'erro': str('ID inválido')}


@app.put("/item/{item_id}")
def update(item_id: int, item:Item):

    conn = psycopg2.connect('postgres://postgres:password@db:5432/postgres')
    cursor = conn.cursor()
  
    try:
        cursor.execute("""
        UPDATE tarefas
        SET tarefa = %s, status = %s
        WHERE id = %s;
        """,  (item.descricao, item.status, item.identificador,))
    except Exception as e:

        return {'erro': str('Erro ao atualizar, verifique se os campos estão corretos')}

    conn.commit()
    conn.close()


@app.delete("/item/{item_id}")
def remove_tarefa(item_id: int):

    conn = psycopg2.connect('postgres://postgres:password@db:5432/postgres')
    cursor = conn.cursor()


    try:
         cursor.execute("""
            SELECT * FROM tarefas WHERE id = %s
            """, (item_id,))
         
         resultado = dict(zip(('identificador', 'descricao', 'status'), cursor.fetchone()))

         if(resultado):
             
             cursor.execute("""
                    DELETE FROM tarefas WHERE id = %s
                            """, (item_id,))
             conn.commit()
             conn.close()
             return{'sucess': str('Tarefa apagada com sucesso')}
            
    except Exception as e:

        return {'erro': str('ID inválido')}
    

    
    
    
    
    



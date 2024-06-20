import os
from fastapi import FastAPI
from pydantic import BaseModel

if not os.path.exists('db.txt'):
    f = open('db.txt', 'w')
    f.close()


app = FastAPI()

class Item(BaseModel):
    identificador: int
    descricao: str
    status: bool


@app.post("/item")
def create(item: Item):

    with open('db.txt', 'r') as f:
        dados = f.readlines()
        for line in dados:
            campos_separados = line.split(',')
            if int(campos_separados[0]) == int(item.identificador):
                return {"erro" : "Mensagem de erro!"}

    with open('db.txt', 'a') as f:
        f.write(f"{item.identificador},{item.descricao},{item.status}\n")

    return {"id": item.identificador, "descricao": item.descricao, "status": item.status}


@app.get("/item")
def list():

    with open('db.txt', 'r') as f:
        dados = f.readlines()

        dados_em_lista = []
        for line in dados:
            campos_separados = line.split(',')
            dados_em_lista.append({
                "identificador":    str(campos_separados[0]),
                "descricao":        str(campos_separados[1]),
                "status":           str(campos_separados[2])
            })

        return dados_em_lista


@app.get("/item/{item_id}")
def get_one(item_id: int):

    with open('db.txt', 'r') as f:
        dados = f.readlines()

        for line in dados:
            campos_separados = line.split(',')
            if int(campos_separados[0]) == item_id:
                return {
                        "identificador":    campos_separados[0],
                        "descricao":        campos_separados[1],
                        "status":           campos_separados[2]
                }

    return {"erro" : "Mensagem de erro!"}


@app.put("/item/{item_id}")
def update(item_id: int, item:Item):
    with open('db.txt', 'r') as f:
        dados = f.readlines()

    with open('db.txt', 'w') as f:
        for line in dados:
            campos_separados = line.split(',')
            if int(campos_separados[0]) != item_id:
                f.write(line)
            else:
                f.write(f"{item.identificador},{item.descricao},{item.status}\n")

    return item.dict()

@app.delete("/item/{item_id}")
def remove_tarefa(item_id: int):

    with open('db.txt', 'r') as f:
        dados = f.readlines()

    with open('db.txt', 'w') as f:

        msg = {'erro' : 'Item não encontrado'}
        for line in dados:
            campos_separados = line.split(',')
            if int(campos_separados[0]) != item_id:
                f.write(line)
            else:
                msg = {'sucesso' : 'Item deletado com sucesso!'}
    return msg
    
    



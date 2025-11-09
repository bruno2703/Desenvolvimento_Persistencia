from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import asyncio

app = FastAPI()

lock = asyncio.Lock()

PRODUTOS_DF = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "nome": ["Mouse Gamer", "Teclado Mecânico", "Monitor HD"],
        "categoria": ["Periférico", "Periférico", "Tela"],
        "preco": [50.00, 350.50, 1200.00]
    }
)

CONTADOR_ID = PRODUTOS_DF["id"].max() + 1


class Produto(BaseModel):
    nome: str
    categoria: str
    preco: float


@app.get("/produtos")
def listar_produtos():
    return PRODUTOS_DF.to_dict(orient="records")

@app.get("/produtos/{id}")
def obter_produto(id: int):
    filtro = PRODUTOS_DF["id"] == id
    produto = PRODUTOS_DF[filtro]
    
    if produto.empty:
        raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
    return produto.to_dict(orient="records")[0]

@app.post("/produtos")
async def cadastrar_produto(produto: Produto):
    async with lock:
        global PRODUTOS_DF, CONTADOR_ID
        
        novo_produto = {
            "id": int(CONTADOR_ID),
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco
        }
        
        PRODUTOS_DF = PRODUTOS_DF._append(novo_produto, ignore_index=True)
        
        CONTADOR_ID = CONTADOR_ID + 1
        
        return {
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": novo_produto
        }

@app.put("/produtos/{id}")
async def atualizar_produto(id: int, produto: Produto):
    global PRODUTOS_DF
    
    async with lock:
        produto_idx = PRODUTOS_DF.index[PRODUTOS_DF["id"] == id]
        
        if produto_idx.empty:
            raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
        PRODUTOS_DF.loc[produto_idx, ["nome", "categoria", "preco"]] = [
            produto.nome, 
            produto.categoria, 
            produto.preco
        ]
        
        return {
            "mensagem": f"Produto {id} atualizado com sucesso!",
            "produto": PRODUTOS_DF.loc[produto_idx].to_dict(orient="records")[0]
        }

@app.delete("/produtos/{id}")
async def remover_produto(id: int):
    global PRODUTOS_DF
    
    async with lock:
        produto_idx = PRODUTOS_DF.index[PRODUTOS_DF["id"] == id]
        
        if produto_idx.empty:
            raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
        PRODUTOS_DF = PRODUTOS_DF.drop(produto_idx).reset_index(drop=True)
        
        return { "mensagem":  f"Produto com {id} apagado com sucesso!"}
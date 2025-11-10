from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware

ARQUIVO_CSV = "produtos.csv"
lock = asyncio.Lock()

app = FastAPI()

# Configuração do CORS 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


# Funcoes de persistencia
def carregar_csv() -> pd.DataFrame:
    try:
        df = pd.read_csv(ARQUIVO_CSV, dtype={'id': 'Int64'})
        df = df.dropna(how='all')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id", "nome", "categoria", "preco"])
    return df

def salvar_csv(df: pd.DataFrame):
    df.to_csv(ARQUIVO_CSV, index=False)



# Variáveis globais
# Inicialização dos dados   
PRODUTOS_DF = carregar_csv()
    
if PRODUTOS_DF.empty:
    CONTADOR_ID = 1
else:
    CONTADOR_ID = PRODUTOS_DF["id"].max() + 1
        
print(f"STATUS: Sistema iniciado. Próximo ID disponível: {CONTADOR_ID}")



class Produto(BaseModel):
    nome: str
    categoria: str
    preco: float

# ENDPOINTS CRUD

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
        
        novo_produto = produto.model_dump()
        novo_produto["id"] = int(CONTADOR_ID)
        
        PRODUTOS_DF = PRODUTOS_DF._append(novo_produto, ignore_index=True)
        salvar_csv(PRODUTOS_DF)
        
        CONTADOR_ID += 1 
        
        return {
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": novo_produto
        }

@app.put("/produtos/{id}")
async def atualizar_produto(id: int, produto: Produto):
    async with lock:
        global PRODUTOS_DF
        produto_idx = PRODUTOS_DF.index[PRODUTOS_DF["id"] == id]
        
        if produto_idx.empty:
            raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
        PRODUTOS_DF.loc[produto_idx, ["nome", "categoria", "preco"]] = [
            produto.nome, 
            produto.categoria, 
            produto.preco
        ]
        
        salvar_csv(PRODUTOS_DF)
        
        return {
            "mensagem": f"Produto {id} atualizado com sucesso!",
            "produto": PRODUTOS_DF.loc[produto_idx].to_dict(orient="records")[0]
        }

@app.delete("/produtos/{id}")
async def remover_produto(id: int):
    async with lock:
        global PRODUTOS_DF
        
        if not (PRODUTOS_DF["id"] == id).any():
             raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
        PRODUTOS_DF = PRODUTOS_DF[PRODUTOS_DF["id"] != id].reset_index(drop=True)
        
        salvar_csv(PRODUTOS_DF)
        
        return { "mensagem":  f"Produto com {id} apagado com sucesso!"}



# Média de preços
@app.get("/produtos/analise/media-precos")
def calcular_media_precos():
    media = PRODUTOS_DF["preco"].mean()
    return {"media_precos": round(media, 2)}

# O produto de maior preço
@app.get("/produtos/analise/maior-preco")
def produto_maior_preco():
    idx_max = PRODUTOS_DF["preco"].idxmax()
    produto = PRODUTOS_DF.loc[idx_max].to_dict()

    return {
        "nome": produto["nome"], 
        "preco": round(produto["preco"], 2)
    }

# O produto de menor preço
@app.get("/produtos/analise/menor-preco")
def produto_menor_preco():
    idx_min = PRODUTOS_DF["preco"].idxmin()
    produto = PRODUTOS_DF.loc[idx_min].to_dict()

    return {
        "nome": produto["nome"], 
        "preco": round(produto["preco"], 2)
    }

# A lista dos produtos mais caros
@app.get("/produtos/analise/acima-media")
def listar_acima_media():
    media = PRODUTOS_DF["preco"].mean()
    filtro_caros = PRODUTOS_DF["preco"] >= media
    produtos_caros = PRODUTOS_DF[filtro_caros]
    
    return {
        "mensagem": f"Produtos com preço igual ou acima da média (R$ {round(media, 2)})",
        "produtos": produtos_caros.to_dict(orient="records")
    }

# A lista dos produtos mais baratos
@app.get("/produtos/analise/abaixo-media")
def listar_abaixo_media():
    media = PRODUTOS_DF["preco"].mean()
    filtro_baratos = PRODUTOS_DF["preco"] < media
    produtos_baratos = PRODUTOS_DF[filtro_baratos]
    
    return {
        "mensagem": f"Produtos com preço abaixo da média (R$ {round(media, 2)})",
        "produtos": produtos_baratos.to_dict(orient="records")
    }
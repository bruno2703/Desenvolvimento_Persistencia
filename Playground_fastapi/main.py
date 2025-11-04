# main.py

# 1. IMPORTAÇÕES NECESSÁRIAS
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio # Para concorrência (Lock)

# 2. VARIÁVEIS GLOBAIS DE CONTROLE
# Variáveis que serão atualizadas ao longo da execução da API
ARQUIVO_CSV = "alunos.csv" # Nome do nosso arquivo
lock = asyncio.Lock()      # Trava de concorrência para escrita segura

# 3. INSTÂNCIA DO APP E MODELAGEM DE DADOS
app = FastAPI() # Inicializa a aplicação FastAPI

# Modelo de dados que define a estrutura de um Aluno (para validação)
class Aluno(BaseModel):
    nome: str
    curso: str
    IRA: float

# main.py (Continue adicionando ao arquivo)

# --- FUNÇÕES DE PERSISTÊNCIA ---

def carregar_csv() -> pd.DataFrame:
    """Carrega o DataFrame do arquivo CSV, ou cria um vazio se não existir."""
    try:
        # Tenta ler o arquivo CSV
        df = pd.read_csv(ARQUIVO_CSV)
    except FileNotFoundError:
        # Se não encontrar, cria um DataFrame vazio com as colunas corretas
        df = pd.DataFrame(columns=["id", "nome", "curso", "IRA"])
    return df

def salvar_csv(df: pd.DataFrame):
    """Salva o DataFrame de volta no arquivo CSV."""
    # index=False evita salvar a coluna de índices do Pandas
    df.to_csv(ARQUIVO_CSV, index=False)


# main.py (Continue adicionando ao arquivo)

# --- ENDPOINT 1: LISTAR TODOS OS ALUNOS (READ) ---
@app.get("/alunos")
def listar_alunos():
    # 1. Carrega os dados mais recentes do CSV
    alunos_df = carregar_csv()
    
    # 2. Converte o DataFrame para o formato JSON (lista de dicionários) e retorna
    return alunos_df.to_dict(orient="records")

# main.py (Continue adicionando ao arquivo)

# --- ENDPOINT 2: CRIAR NOVO ALUNO (CREATE) ---
@app.post("/alunos")
async def criar_aluno(aluno: Aluno):
    # A trava (Lock) garante que apenas um cliente modifique os dados por vez
    async with lock:
        # 1. Carrega os dados mais recentes do disco
        alunos_df = carregar_csv()
        
        # 2. Geração do próximo ID (Simulando a base de dados)
        if alunos_df.empty:
            proximo_id = 1
        else:
            # Pega o maior ID existente e soma 1 (robusto contra IDs deletados)
            proximo_id = alunos_df["id"].max() + 1
        
        # 3. Monta o dicionário da nova linha
        novo_aluno = {
            "id": proximo_id,
            "nome": aluno.nome,
            "curso": aluno.curso,
            "IRA": aluno.IRA
        }
        
        # 4. Insere o novo objeto (dicionário) no DataFrame
        alunos_df = alunos_df._append(novo_aluno, ignore_index=True)
        
        # 5. Salva a modificação no CSV
        salvar_csv(alunos_df)
        
        return {
            "mensagem": "Aluno criado com sucesso!",
            "aluno": novo_aluno
        }
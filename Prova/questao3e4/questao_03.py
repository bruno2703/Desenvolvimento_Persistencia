
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import time

app = FastAPI()

#variaveis globais 
contador_id = 3
alunos_df = pd.DataFrame(
    {
        "nome": ["Fulano", "Sicrano", "Beltrano"],
        "nota": [8.5, 7.0, 9.0]
    }
)

class NotaAluno(BaseModel):
    nome: str
    nota: float


@app.post("/alunos") 
def adicionar_ou_atualizar_aluno(nota_aluno: NotaAluno):
    global alunos_df
    aluno_existente = alunos_df[alunos_df["nome"] == nota_aluno.nome]

    if not aluno_existente.empty:
        alunos_df.loc[alunos_df["nome"] == nota_aluno.nome, "nota"] = nota_aluno.nota
        return {"mensagem": "Nota do aluno atualizada com sucesso."}
    else:
        novo_aluno = pd.DataFrame({"nome": [nota_aluno.nome], "nota": [nota_aluno.nota]})
        alunos_df = alunos_df._append(novo_aluno, ignore_index=True)
        return {"mensagem": "Aluno adicionado com sucesso."}


@app.get("/alunos/{nome}")
def obter_nota_aluno(nome: str):
    global alunos_df
    aluno = alunos_df[alunos_df["nome"] == nome]

    if aluno.empty:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    nota = aluno["nota"].values[0]
    return {"nome": nome, "nota": nota}


#Questao 4

@app.get("/alunos")
def listar_alunos():
    global alunos_df
    return alunos_df.to_dict(orient="records")


